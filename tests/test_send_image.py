import os
import sys
import tempfile
from PIL import Image
import pytest

# Ensure project root for direct runs
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from pages.page_factory import PageFactory


def _create_temp_png() -> str:
    fd, path = tempfile.mkstemp(suffix=".png")
    os.close(fd)
    img = Image.new("RGB", (16, 16), color=(255, 0, 0))
    img.save(path, "PNG")
    return path


@pytest.mark.parametrize(
    "viewport",
    [
        ("desktop", 1366, 900),
        ("mobile", 700, 900),
    ],
)
def test_upload_image_and_type_then_submit(driver, base_url, viewport):
    label, width, height = viewport
    driver.set_window_size(width, height)

    driver.get(base_url)

    chat_page = PageFactory.create_chat_page(driver)

    image_path = _create_temp_png()
    try:
        chat_page.upload_image_and_submit(image_path, "messi")
    finally:
        if os.path.exists(image_path):
            os.remove(image_path)

    # End test gracefully
    assert True


