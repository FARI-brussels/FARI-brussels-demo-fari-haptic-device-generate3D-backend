# 3d Model generation api for the Haptic Device Demo 

This is a version of [Shap-E: Generating Conditional 3D Implicit Functions](https://arxiv.org/abs/2305.02463), extended with an API in order to serve a Unity demonstration for an haptic device. The unity demonstration allows you to generate a 3D model from a prompt, to load it in unity and to "feel it" through the force feedback of the haptic device.

## API Documentation

### Endpoint: `/generate`

Generates a single 3D model based on a given text prompt and saves it as an .obj file at a specified path.

#### Method: `POST`

#### URL: `http://<your-server-address>:5000/generate`

#### Request Body (JSON):

| Parameter | Type   | Description                                 |
|-----------|--------|---------------------------------------------|
| prompt    | string | The text prompt to generate the 3D model(s).|
|save_path	|string	 |(Optional) The file path where the model is saved.|

If save_path is not provided, the file will be saved in the default directory where the server is running.

#### Response Body (JSON):

| Parameter  | Type  | Description                                       |
|------------|-------|---------------------------------------------------|
| file_path  | string | The path to the generated .obj file.|

#### Status Codes:

- `200 OK`: Request was successful, and 3D models were generated.
- `4XX`: Client errors (bad request data).
- `5XX`: Server errors (issues with model generation or server configuration).

---

## Example Usage:

### Curl

```bash
curl -X POST -H "Content-Type: application/json" -d "{\"prompt\":\"a shark\", \"save_path\":\"C:\\desired\\path\\for\\model\"}" http://localhost:5000/generate
```

## C# (using HttpClient)
```csharp
using System;
using System.Net.Http;
using System.Text;
using System.Threading.Tasks;
using Newtonsoft.Json; // Ensure Newtonsoft.Json is installed: Install-Package Newtonsoft.Json

namespace APIClient
{
    class Program
    {
        static readonly HttpClient client = new HttpClient();

        static async Task Main()
        {
            var url = "http://localhost:5000/generate";
            var requestData = new 
            { 
                prompt = "a shark",
                save_path = "C:\\desired\\path\\for\\model"
            };
            
            var json = JsonConvert.SerializeObject(requestData);
            var data = new StringContent(json, Encoding.UTF8, "application/json");

            HttpResponseMessage response = await client.PostAsync(url, data);
            if(response.IsSuccessStatusCode)
            {
                string result = await response.Content.ReadAsStringAsync();
                Console.WriteLine("Generated model path: " + result);
            }
            else
            {
                Console.WriteLine("Error: " + response.StatusCode);
            }
        }
    }
}

```


# Samples

Here are some highlighted samples from our text-conditional model. For random samples on selected prompts, see [samples.md](samples.md).

<table>
    <tbody>
        <tr>
            <td align="center">
                <img src="samples/a_chair_that_looks_like_an_avocado/2.gif" alt="A chair that looks like an avocado">
            </td>
            <td align="center">
                <img src="samples/an_airplane_that_looks_like_a_banana/3.gif" alt="An airplane that looks like a banana">
            </td align="center">
            <td align="center">
                <img src="samples/a_spaceship/0.gif" alt="A spaceship">
            </td>
        </tr>
        <tr>
            <td align="center">A chair that looks<br>like an avocado</td>
            <td align="center">An airplane that looks<br>like a banana</td>
            <td align="center">A spaceship</td>
        </tr>
        <tr>
            <td align="center">
                <img src="samples/a_birthday_cupcake/3.gif" alt="A birthday cupcake">
            </td>
            <td align="center">
                <img src="samples/a_chair_that_looks_like_a_tree/2.gif" alt="A chair that looks like a tree">
            </td>
            <td align="center">
                <img src="samples/a_green_boot/3.gif" alt="A green boot">
            </td>
        </tr>
        <tr>
            <td align="center">A birthday cupcake</td>
            <td align="center">A chair that looks<br>like a tree</td>
            <td align="center">A green boot</td>
        </tr>
        <tr>
            <td align="center">
                <img src="samples/a_penguin/1.gif" alt="A penguin">
            </td>
            <td align="center">
                <img src="samples/ube_ice_cream_cone/3.gif" alt="Ube ice cream cone">
            </td>
            <td align="center">
                <img src="samples/a_bowl_of_vegetables/2.gif" alt="A bowl of vegetables">
            </td>
        </tr>
        <tr>
            <td align="center">A penguin</td>
            <td align="center">Ube ice cream cone</td>
            <td align="center">A bowl of vegetables</td>
        </tr>
    </tbody>
<table>

# Installation

```
git clone https://github.com/FARI-brussels/demo-fari-haptic-device-generate3D-backend.git
cd demo-fari-haptic-device-generate3D-backend
pip install -e .
pip install Flask
```

Note : It is advised to run the code in a conda environement


# Usage

```
cd shap_e/api
python generate.py
```

Note : It is advised to run the code in a conda environement