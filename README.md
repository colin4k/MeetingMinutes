# User Manual

Team : Théo Pirouelle

<a href="https://www.python.org/">
  <img src="https://img.shields.io/badge/language-python-blue?style=flat-square" alt="laguage-python" />
</a>

---

## Preamble

To use the script, you'll need an [OpenAI API key](https://platform.openai.com/account/api-keys) for Whisper and GPT-4.
You'll need to create a `.env` file with the `API_KEY` variable with your API key for the script to work properly.

The script on the repository is configured in French; it's easy to modify the script to adapt it to another language (just translate the few instructions given to GPT).

> [!IMPORTANT]
> To use the script, you need to be connected to the Internet so that it can call the OpenAI API.

You will also need to install the necessary :
```bash
sudo apt-get update

sudo apt install ffmpeg

sudo apt install python3
sudo apt install python3-pip

pip3 install openai
pip3 install python-docx
pip3 install pydub
pip3 install ffmpeg-python
```

> [!NOTE]
> For information, the code has been developed and works with the following library versions:
> | Library | Version |
> | --- | --- |
> | openai | 0.28.0 |
> | python-docx | 1.1.0 |
> | pydub | 0.25.1 |
> | ffmpeg-python | 0.2.0 |

## Usage

```bash
src/script.sh <file_name> [-ss <start_time>] [-to <end_time>]
```

> [!WARNING]
> The file must be a `.mp3` or `.mkv`.

When you run the script, it will ask you whether you want to run the complete script or just the transcript.
The complete script includes transcript, summary, key points and action points.

You can change the model used in the code by modifying the `model_gpt` variable. You can find a list of the different GPT models supported on the [OpenAI site](https://platform.openai.com/docs/guides/function-calling), along with the methods of use for API calls.

## Performance

Here are the performances I've seen in use:

| Model | Recording time | Treatment duration | Cost |
| --- | --- | --- | --- |
| gpt-4 | 1min | 40sec |  |
| gpt-4 | 3min | 2min | 0.07$ |
| gpt-4 | 10min | 3min30 | 0.11$ |
| gpt-4-1106-preview | 10min | 1min20 | 0.17$ |
| gpt-4 | 15min |  | 0.49$ |
| gpt-4-1106-preview | 16min37 | 3min20 | 0.27$ |
| gpt-4-1106-preview | 17min32 | 2min13 | 0.26$ |
| gpt-4-1106-preview | 18min35 | 3min28 | 0.22$ |
| gpt-4 | 27min17 | 4min15 | 0.79$ |

You can find costs for the various models (including Whisper and GPT-4) on the [OpenAI website](https://openai.com/pricing).

You can also find all your consumption for the current month, as well as your payment history, on the [Usage page](https://platform.openai.com/usage).
