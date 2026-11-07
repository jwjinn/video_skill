"""Compose an HIS01-style silent video from existing chart clips."""
import argparse
import hashlib
import json
import re
import shutil
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
FPS = 30


def run(args):
    result = subprocess.run(args, cwd=HERE, capture_output=True, text=True)
    if result.returncode:
        raise RuntimeError(result.stderr[-8000:])
    return result.stdout


def probe(path):
    return json.loads(run(["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(path)]))


def frames(seconds):
    value = float(seconds) * FPS
    if value < 1 or abs(value - round(value)) > 0.001:
        raise ValueError("Durations must be positive multiples of 1/30 second")
    return round(value)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--redraw", action="store_true", help="Regenerate text cards using Pillow")
    parser.add_argument("--output", type=Path, help="Output MP4 path (default: output/<id>.mp4)")
    args = parser.parse_args()
    for tool in ("ffmpeg", "ffprobe"):
        if not shutil.which(tool):
            raise RuntimeError(f"Install {tool} and add it to PATH")
    episode = json.loads((HERE / "episode.json").read_text(encoding="utf-8"))
    ids = [episode["id"], *[c["chart"] for c in episode["chapters"]]]
    if any(not re.fullmatch(r"[A-Za-z0-9_-]+", item) for item in ids):
        raise ValueError("Episode and chart IDs must contain only letters, digits, _ or -")
    chapters = episode["chapters"]
    if not chapters or len(set(c["chart"] for c in chapters)) != len(chapters):
        raise ValueError("Supply at least one chapter and unique chart IDs")
    timing = {"intro": 3, "example": 5, "chart": 12, "outro": 5, **episode.get("timing", {})}
    counts = {key: frames(value) for key, value in timing.items()}
    if counts["chart"] % 2:
        raise ValueError("Chart duration must split into two equal frame-aligned caption segments")
    for chapter in chapters:
        if len(chapter["captions"]) != 2:
            raise ValueError("Each chart needs exactly two captions")
        chart = HERE / "charts" / (chapter["chart"] + ".mp4")
        if not chart.is_file():
            raise FileNotFoundError(f"Missing {chart.name}. Render chart inputs first (see references/rendering.md).")
        info = probe(chart)
        video = next(s for s in info["streams"] if s["codec_type"] == "video")
        if (video["width"], video["height"]) != (1080, 1350) or float(info["format"]["duration"]) < 19.5:
            raise ValueError(f"{chart.name}: expected 1080x1350 and at least 19.5 seconds")
    work = HERE / "work"
    work.mkdir(exist_ok=True)
    assets = HERE / "assets"
    if args.redraw:
        assets.mkdir(exist_ok=True)
        import layout
        layout.card(episode, False).save(assets / "intro.png")
        layout.card(episode, True).save(assets / "outro.png")
        for chapter in chapters:
            name = chapter["chart"]
            layout.example_card(episode, chapter).save(assets / f"{name}-example.png")
            for index in (0, 1):
                layout.overlay(episode, chapter, index).save(assets / f"{name}-caption-{index}.png")
    encode = ["-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p"]

    def still(name, count):
        out = work / (name + ".mp4")
        run(["ffmpeg", "-v", "error", "-y", "-loop", "1", "-framerate", str(FPS), "-i", str(assets / (name + ".png")),
             "-frames:v", str(count), *encode, str(out)])
        return out

    parts = [still("intro", counts["intro"])]
    for chapter in chapters:
        name = chapter["chart"]
        parts.append(still(name + "-example", counts["example"]))
        for index in (0, 1):
            start = 1.5 + index * 9
            factor = float(timing["chart"]) / 18
            filters = (f"[0:v]trim=start={start}:end={start + 9},setpts=(PTS-STARTPTS)*{factor},"
                       "setsar=1,crop=1080:1140:0:114,scale=972:1026,"
                       "pad=1080:1350:54:108:color=0x10181c[b];"
                       "[b][1:v]overlay=0:0,crop=1080:1350:0:0,setsar=1[out]")
            out = work / f"{name}-{index}.mp4"
            run(["ffmpeg", "-v", "error", "-y", "-i", str(HERE / "charts" / (name + ".mp4")),
                 "-loop", "1", "-framerate", str(FPS), "-i", str(assets / f"{name}-caption-{index}.png"),
                 "-filter_complex", filters, "-map", "[out]", "-frames:v", str(counts["chart"] // 2),
                 "-r", str(FPS), *encode, str(out)])
            parts.append(out)
    parts.append(still("outro", counts["outro"]))
    listing = work / "concat.txt"
    listing.write_text("\n".join("file '" + part.name + "'" for part in parts) + "\n", encoding="utf-8")
    out = args.output.resolve() if args.output else HERE / "output" / (episode["id"] + ".mp4")
    out.parent.mkdir(parents=True, exist_ok=True)
    run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(listing),
         "-an", "-c", "copy", "-movflags", "+faststart", str(out)])
    info = probe(out)
    expected = counts["intro"] + counts["outro"] + len(chapters) * (counts["example"] + counts["chart"])
    video = info["streams"][0]
    if len(info["streams"]) != 1 or video["codec_type"] != "video":
        raise RuntimeError("Expected a silent video with one video stream")
    if (video["width"], video["height"], video["r_frame_rate"], int(video["nb_frames"])) != (1080, 1350, "30/1", expected):
        raise RuntimeError("Output dimensions, frame rate or frame count differ from the timeline")
    run(["ffmpeg", "-v", "error", "-i", str(out), "-f", "null", "-"])
    record = {"video": out.name, "width": 1080, "height": 1350, "fps": FPS, "frames": expected,
              "seconds": expected / FPS, "audio": False, "fullDecode": "passed",
              "sha256": hashlib.sha256(out.read_bytes()).hexdigest(), "synthetic": episode.get("synthetic", False),
              "historicalClaimsVerified": False,
              "note": "Media validation only; compare data and narrative with original evidence separately."}
    out.with_name(out.stem + "-validation.json").write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    print(out)


if __name__ == "__main__":
    main()
