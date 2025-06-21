import subprocess, time

def open_with_video_player(url, subtitle_url=None):
    """Video Oynatıcı"""
    try:
        cmd = [
            'mpv',
            '--fullscreen',
            '--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/137.0.0.0 Safari/537.36',
            '--referrer=https://yeshi.eu.org/'
        ]

        if subtitle_url:
            cmd += ['--sub-file=' + subtitle_url]
        cmd.append(url)

        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL)
    except subprocess.CalledProcessError as e:
        print("Oynatılırken Hata Oluştu!", e)
        time.sleep(10)
