import azure.functions as func
import nltk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
import os
import json
import working_orchestrator



# Create the Function App instance
app = func.FunctionApp()


def ensure_nltk_data():
    """Ensure NLTK data is available, downloading if necessary."""
    try:
        data_path = os.path.join(os.environ.get("TEMP", "/tmp"), "nltk_data")
        nltk.data.path.append(data_path)

        # Check for and download required NLTK resources
        try:
            nltk.data.find("tokenizers/punkt")
            nltk.data.find("taggers/averaged_perceptron_tagger")
            nltk.data.find("tokenizers/punkt_tab")  # Check for punkt_tab
            nltk.data.find("taggers/averaged_perceptron_tagger_eng")  # Check for averaged_perceptron_tagger_eng
        except LookupError:
            nltk.download("punkt", download_dir=data_path, quiet=True)
            nltk.download("averaged_perceptron_tagger", download_dir=data_path, quiet=True)
            nltk.download("punkt_tab", download_dir=data_path, quiet=True)  # Download punkt_tab if not found
            nltk.download("averaged_perceptron_tagger_eng", download_dir=data_path, quiet=True)  # Download averaged_perceptron_tagger_eng
    except Exception as e:
        print(f"Error setting up NLTK data: {str(e)}")


def analyze_verbs(text_chunk):
    """Analyze verbs in a chunk of text and categorize them by tense."""
    ensure_nltk_data()

    try:
        tokens = word_tokenize(text_chunk)
        tagged = pos_tag(tokens)
    except Exception as e:
        return {"error": f"Text processing failed: {str(e)}"}

    verb_counts = {
        "past": 0,  # VBD, VBN
        "present": 0,  # VBP, VBZ, VBG
        "future": 0,  # 'will' followed by VB
        "base": 0,  # VB
        "gerund": 0,  # VBG
        "participle": 0,  # VBN
    }

    for word, tag in tagged:
        if tag in ["VBD", "VBN"]:
            verb_counts["past"] += 1
        elif tag in ["VBP", "VBZ"]:
            verb_counts["present"] += 1
        elif tag == "VB":
            verb_counts["base"] += 1
        elif tag == "VBG":
            verb_counts["gerund"] += 1
        elif tag == "VBN":
            verb_counts["participle"] += 1

    # Detect future tense (e.g., "will go")
    for i in range(len(tagged) - 1):
        if tagged[i][0].lower() == "will" and tagged[i + 1][1].startswith("VB"):
            verb_counts["future"] += 1

    return verb_counts


# HTTP Trigger Function
@app.route(route="analyze_verbs", methods=["POST"], auth_level=func.AuthLevel.ANONYMOUS)
def analyze_verbs_handler(req: func.HttpRequest) -> func.HttpResponse:
    """Handles HTTP requests for verb analysis."""
    try:
        req_body = req.get_json()
        text = req_body.get("text")

        if not text:
            return func.HttpResponse(
                "Please provide text in the request body", status_code=400
            )

        result = analyze_verbs(text)
        return func.HttpResponse(
            json.dumps(result),
            mimetype="application/json",
            status_code=200,
        )

    except ValueError:
        return func.HttpResponse("Invalid JSON in request body", status_code=400)

    except Exception as e:
        return func.HttpResponse(f"Error: {str(e)}", status_code=500)

