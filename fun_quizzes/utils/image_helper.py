import tempfile
import requests
from django.core.files import File
from django.utils import timezone

def download_and_save_image(image_url, test_id, model_instance, field_name='result_image'):
    try:
        img_temp = tempfile.NamedTemporaryFile(delete=True)
        img_temp.write(requests.get(image_url).content)
        img_temp.flush()
        filename = f"past_life_{test_id}_{timezone.now().strftime('%Y%m%d%H%M%S')}.png"
        getattr(model_instance, field_name).save(filename, File(img_temp))
        return True
    except Exception:
        return False