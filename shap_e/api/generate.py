from flask import Flask, request, jsonify
import torch
from shap_e.diffusion.sample import sample_latents
from shap_e.diffusion.gaussian_diffusion import diffusion_from_config
from shap_e.models.download import load_model, load_config
from shap_e.util.notebooks import decode_latent_mesh
import os

app = Flask(__name__)

# Load models and configurations outside of the request to save time.
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
xm = load_model('transmitter', device=device)
model = load_model('text300M', device=device)
diffusion = diffusion_from_config(load_config('diffusion'))

@app.route('/generate', methods=['POST'])
def generate():
    content = request.json
    prompt = content['prompt']
    batch_size = 1
    guidance_scale = 15.0

    # Sample latents based on the prompt.
    latents = sample_latents(
        batch_size=batch_size,
        model=model,
        diffusion=diffusion,
        guidance_scale=guidance_scale,
        model_kwargs=dict(texts=[prompt] * batch_size),
        progress=False,
        clip_denoised=True,
        use_fp16=True,
        use_karras=True,
        karras_steps=64,
        sigma_min=1e-3,
        sigma_max=160,
        s_churn=0,
    )

    # Save the latents as meshes.
    file_paths = []
    for i, latent in enumerate(latents):
        t = decode_latent_mesh(xm, latent).tri_mesh()
        obj_filename = f'example_mesh_{i}.obj'
        with open(obj_filename, 'w') as f:
            t.write_obj(f)
        file_paths.append(obj_filename)

    # Return the file paths in the response.
    return jsonify({'file_paths': file_paths})

if __name__ == '__main__':
    app.run(debug=True)
