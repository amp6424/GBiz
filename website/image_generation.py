# importing needed modules
from io import BytesIO
import IPython
import json
import os
from PIL import Image
import requests
import time


class PostGenerator:

    def __init__(self, prompt, type="post"):
        # apikey
        self.STABILITY_KEY = "" # Replace it with your API Key
        # Stable Image Ultra
        prompt = prompt
        negative_prompt = "" #@param {type:"string"}
        if type == "post":
            aspect_ratio = "1:1" #@param ["21:9", "16:9", "3:2", "5:4", "1:1", "4:5", "2:3", "9:16", "9:21"]
        else:
            aspect_ratio = "16:9"
        seed = 0 #@param {type:"integer"}
        output_format = "jpeg" #@param ["webp", "jpeg", "png"]

        host = f"https://api.stability.ai/v2beta/stable-image/generate/ultra"

        params = {
            "prompt" : prompt,
            "negative_prompt" : negative_prompt,
            "aspect_ratio" : aspect_ratio,
            "seed" : seed,
            "output_format": output_format
        }

        response = self.send_generation_request(host,params)

        # Decode response
        output_image = response.content
        finish_reason = response.headers.get("finish-reason")
        seed = response.headers.get("seed")

        # Check for NSFW classification
        if finish_reason == 'CONTENT_FILTERED':
            raise Warning("Generation failed NSFW classifier")

        # Save and display result
        generated = f"./static/images/generated_{seed}.{output_format}"
        with open(generated, "wb") as f:
            f.write(output_image)
        self.generated = generated
        print(f"Saved image {generated}")

        # output.no_vertical_scroll()
        print("Result image:")
        IPython.display.display(Image.open(generated))

    # defining functions
    def send_generation_request(self, host, params):
        headers = {
            "Accept": "image/*",
            "Authorization": f"Bearer {self.STABILITY_KEY}"
        }

        # Encode parameters
        files = {}
        image = params.pop("image", None)
        mask = params.pop("mask", None)
        if image is not None and image != '':
            files["image"] = open(image, 'rb')
        if mask is not None and mask != '':
            files["mask"] = open(mask, 'rb')
        if len(files)==0:
            files["none"] = ''

        # Send request
        print(f"Sending REST request to {host}...")
        response = requests.post(host, headers=headers, files=files, data=params)
        if not response.ok:
            raise Exception(f"HTTP {response.status_code}: {response.text}")

        return response

    def send_async_generation_request(self, host,params):
        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {STABILITY_KEY}"
        }

        # Encode parameters
        files = {}
        if "image" in params:
            image = params.pop("image")
            files = {"image": open(image, 'rb')}

        # Send request
        print(f"Sending REST request to {host}...")
        response = requests.post(host, headers=headers, files=files, data=params)
        if not response.ok:
            raise Exception(f"HTTP {response.status_code}: {response.text}")

        # Process async response
        response_dict = json.loads(response.text)
        generation_id = response_dict.get("id", None)
        assert generation_id is not None, "Expected id in response"

        # Loop until result or timeout
        timeout = int(os.getenv("WORKER_TIMEOUT", 500))
        start = time.time()
        status_code = 202
        while status_code == 202:
            response = requests.get(
                f"{host}/result/{generation_id}",
                headers={
                    **headers,
                    "Accept": "image/*"
                },
            )

            if not response.ok:
                raise Exception(f"HTTP {response.status_code}: {response.text}")
            status_code = response.status_code
            time.sleep(10)
            if time.time() - start > timeout:
                raise Exception(f"Timeout after {timeout} seconds")

        return response

if __name__ == "__main__":
    prompt = input("Enter description for the image:\n")
    createPost = PostGenerator(prompt)

'''
PROMPTS:
    - Create me a post for my brand BudgetStitch, which connect local fashion designers which fashion enthusiasts and genz audience, create me a launch post on instagram for it. I want a maniqunie with pink cute skirt on it. And the theme of the post should be pink and white! I want few texts on it and it should be exciting, elegant and beautiful.
    - Create a post for Makeup brand, for marketing their offer of 30% across all categories valid for 1 week only! I want post to be creative, graphical and youthful. it should show the offer clearly and valid. It should create excitement and should grow the brand business and awareness. the idea and the post should be out of the box!
'''