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
    save_path = content.get('save_path', '')  # Get the save_path if provided, else default to empty string.
    batch_size = 1
    guidance_scale = 15.0

    # Validate save_path
    if save_path and not os.path.isdir(save_path):
        os.makedirs(save_path, exist_ok=True)  # Create the directory if it does not exist

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

    # Save the latent as a mesh (only one).
    latent = latents[0]  # Assuming only one latent is generated.
    t = decode_latent_mesh(xm, latent).tri_mesh()
    file_name = 'generated_model.obj'
    full_path = os.path.join(save_path, file_name) if save_path else file_name
    with open(full_path, 'w') as f:
        t.write_obj(f)

    # Return the file path in the response.
    return jsonify({'file_path': full_path})

if __name__ == '__main__':
    app.run(debug=True)
