import os
import pandas as pd
from tqdm import tqdm
from sentinelhub import (
    SHConfig, BBox, CRS,
    SentinelHubRequest, DataCollection, MimeType
)
from dotenv import load_dotenv
from PIL import Image

load_dotenv()

config = SHConfig()
config.sh_client_id = os.getenv("SH_CLIENT_ID")
config.sh_client_secret = os.getenv("SH_CLIENT_SECRET")

evalscript = """
//VERSION=3
function setup() {
  return {
    input: ["B02", "B03", "B04"],
    output: { bands: 3 }
  };
}
function evaluatePixel(sample) {
  return [sample.B04, sample.B03, sample.B02];
}
"""

def fetch_images(csv_path, save_dir, limit=3000):
    df = pd.read_csv(csv_path)
    os.makedirs(save_dir, exist_ok=True)

    for i, row in tqdm(df.iterrows(), total=min(len(df), limit)):
        if i >= limit:
            break

        pid = row["id"]
        lat = row["lat"]
        lon = row["long"]

        img_path = os.path.join(save_dir, f"{pid}.png")
        if os.path.exists(img_path):
            continue

        bbox = BBox(
            bbox=[lon-0.002, lat-0.002, lon+0.002, lat+0.002],
            crs=CRS.WGS84
        )

        request = SentinelHubRequest(
            evalscript=evalscript,
            input_data=[
                SentinelHubRequest.input_data(
                    data_collection=DataCollection.SENTINEL2_L2A,
                    time_interval=("2023-06-01", "2023-06-30"),
                    mosaicking_order="mostRecent"
                )
            ],
            responses=[
                SentinelHubRequest.output_response("default", MimeType.PNG)
            ],
            bbox=bbox,
            size=(256, 256),
            config=config
        )

        image = request.get_data()[0]
        Image.fromarray(image).save(img_path)

if __name__ == "__main__":
    fetch_images("train.csv", "images/train")
    fetch_images("test.csv", "images/test")
