from pathlib import Path
from PIL import Image, ImageOps
import imageio_ffmpeg
import subprocess

def build_video(images, output_path: Path, fps: int = 24, seconds_per_scene: int = 3):
    """Encode a simple silent MP4 slideshow using the bundled FFmpeg binary."""
    if not images:
        raise ValueError("No images to encode")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    # Create a temporary concat file. Each image is shown for a few seconds.
    concat_path = output_path.parent / "ffmpeg_concat.txt"
    lines = []
    for p in images:
        lines.append(f"file '{Path(p).resolve().as_posix()}'")
        lines.append(f"duration {seconds_per_scene}")
    lines.append(f"file '{Path(images[-1]).resolve().as_posix()}'")
    concat_path.write_text("\n".join(lines), encoding="utf-8")
    cmd = [ffmpeg, "-y", "-f", "concat", "-safe", "0", "-i", str(concat_path),
           "-vf", "scale=960:540:force_original_aspect_ratio=decrease,pad=960:540:(ow-iw)/2:(oh-ih)/2,format=yuv420p",
           "-r", str(fps), "-c:v", "libx264", "-preset", "ultrafast", "-movflags", "+faststart",
           "-pix_fmt", "yuv420p", str(output_path)]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
    try:
        concat_path.unlink(missing_ok=True)
    except Exception:
        pass
    if result.returncode != 0 or not output_path.exists():
        raise RuntimeError((result.stderr or "FFmpeg could not encode video")[-800:])
    return output_path
