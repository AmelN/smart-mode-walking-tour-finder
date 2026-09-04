from flask import Flask, render_template_string, request
from hai_agents import Client
from dotenv import load_dotenv
import html
from datetime import datetime
import re

load_dotenv()

app = Flask(__name__)

client = Client()


HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <title>Smart Mode | Walking Tour Finder</title>

    <style>
        * {
            box-sizing: border-box;
        }

        body {
            margin: 0;
            font-family:
                -apple-system,
                BlinkMacSystemFont,
                "Segoe UI",
                Roboto,
                Helvetica,
                Arial,
                sans-serif;
            background: #f5f5f7;
            color: #18181b;
        }

        .page {
            min-height: 100vh;
            padding: 64px 24px;
        }

        .container {
            max-width: 760px;
            margin: 0 auto;
        }

        .header {
            text-align: center;
            margin-bottom: 32px;
        }

        .logo {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 42px;
            height: 42px;
            border-radius: 12px;
            background: #18181b;
            color: white;
            font-size: 20px;
            margin-bottom: 16px;
        }

        h1 {
            margin: 0 0 8px;
            font-size: 32px;
            letter-spacing: -0.7px;
        }

        .subtitle {
            color: #71717a;
            font-size: 16px;
        }

        .card {
            background: white;
            border: 1px solid #e4e4e7;
            border-radius: 20px;
            padding: 32px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.05);
        }

        .field {
            margin-bottom: 22px;
        }

        label {
            display: block;
            margin-bottom: 8px;
            font-size: 14px;
            font-weight: 600;
            color: #3f3f46;
        }

        input,
        select {
            width: 100%;
            height: 48px;
            padding: 0 14px;
            border: 1px solid #d4d4d8;
            border-radius: 10px;
            background: white;
            color: #18181b;
            font-size: 15px;
            outline: none;
        }

        input:focus,
        select:focus {
            border-color: #71717a;
            box-shadow: 0 0 0 3px rgba(24, 24, 27, 0.08);
        }

        .row {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 18px;
        }

        .actions {
            margin-top: 28px;
        }

        button {
            width: 100%;
            height: 50px;
            border: 0;
            border-radius: 11px;
            font-size: 15px;
            font-weight: 600;
            cursor: pointer;
            transition: opacity 0.15s, transform 0.1s;
        }

        button:active {
            transform: scale(0.99);
        }

        button:disabled {
            cursor: wait;
            opacity: 0.65;
        }

        .manual {
            background: #f4f4f5;
            color: #3f3f46;
        }

        .divider {
            display: flex;
            align-items: center;
            gap: 14px;
            margin: 18px 0;
            color: #a1a1aa;
            font-size: 13px;
        }

        .divider::before,
        .divider::after {
            content: "";
            height: 1px;
            background: #e4e4e7;
            flex: 1;
        }

        .smart {
            background: #18181b;
            color: white;
        }

        .smart:hover {
            background: #27272a;
        }

        .loading-state {
            display: none;
            margin-top: 24px;
            padding: 18px;
            border: 1px solid #e4e4e7;
            border-radius: 12px;
            background: #fafafa;
            text-align: center;
            color: #52525b;
        }

        .loading-state.visible {
            display: block;
        }

        .spinner {
            width: 20px;
            height: 20px;
            margin: 0 auto 10px;
            border: 2px solid #d4d4d8;
            border-top-color: #18181b;
            border-radius: 50%;
            animation: spin 0.8s linear infinite;
        }

        @keyframes spin {
            to {
                transform: rotate(360deg);
            }
        }

        .result {
            margin-top: 32px;
        }

        .result-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 12px;
            margin-bottom: 16px;
        }

        .result-title {
            font-size: 19px;
            font-weight: 700;
        }

        .badge {
            display: inline-flex;
            align-items: center;
            padding: 6px 10px;
            border-radius: 999px;
            background: #f4f4f5;
            color: #52525b;
            font-size: 12px;
            font-weight: 600;
            white-space: nowrap;
        }

        .recommendation {
            border: 1px solid #e4e4e7;
            border-radius: 16px;
            overflow: hidden;
            background: white;
            box-shadow: 0 6px 18px rgba(0, 0, 0, 0.04);
        }

        .recommendation-top {
            padding: 24px;
        }

        .recommended-label {
            margin-bottom: 8px;
            font-size: 12px;
            font-weight: 700;
            color: #71717a;
            text-transform: uppercase;
            letter-spacing: 0.6px;
        }

        .tour-name {
            margin-bottom: 18px;
            font-size: 22px;
            font-weight: 700;
            letter-spacing: -0.3px;
        }

        .details {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 12px;
        }

        .detail {
            padding: 13px;
            border-radius: 10px;
            background: #f7f7f8;
        }

        .detail-label {
            margin-bottom: 4px;
            color: #71717a;
            font-size: 11px;
            font-weight: 600;
            text-transform: uppercase;
        }

        .detail-value {
            font-size: 14px;
            font-weight: 600;
        }

        .recommendation-actions {
            display: flex;
            gap: 10px;
            padding: 16px 24px;
            border-top: 1px solid #e4e4e7;
            background: #fafafa;
        }

        .secondary-button,
        .primary-button {
            flex: 1;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            height: 42px;
            border-radius: 9px;
            text-decoration: none;
            font-size: 13px;
            font-weight: 600;
        }

        .secondary-button {
            background: white;
            border: 1px solid #d4d4d8;
            color: #3f3f46;
        }

        .primary-button {
            background: #18181b;
            color: white;
        }

        .agent-output {
            margin-top: 14px;
            padding: 18px;
            border-radius: 12px;
            background: #f7f7f8;
            color: #52525b;
            font-size: 13px;
            line-height: 1.6;
        }

        .agent-output summary {
            cursor: pointer;
            font-weight: 600;
            color: #3f3f46;
        }

        .error {
            margin-top: 24px;
            padding: 16px;
            border: 1px solid #fecaca;
            border-radius: 10px;
            background: #fef2f2;
            color: #991b1b;
            font-size: 14px;
        }

        @media (max-width: 600px) {
            .page {
                padding: 32px 16px;
            }

            .card {
                padding: 22px;
            }

            .row,
            .details {
                grid-template-columns: 1fr;
            }

            .recommendation-actions {
                flex-direction: column;
            }
        }
    </style>
</head>

<body>

<div class="page">

    <div class="container">

        <div class="header">

            <div class="logo">✦</div>

            <h1>Walking Tour Finder</h1>

            <div class="subtitle">
                Find the right tour without navigating the site yourself.
            </div>

        </div>

        <div class="card">

            <form method="POST" id="smart-form">

                <div class="field">

                    <label for="destination">
                        Destination
                    </label>

                    <input
                        id="destination"
                        name="destination"
                        value="{{ destination }}"
                        placeholder="Barcelona"
                        required
                    >

                </div>

                <div class="field">

                    <label for="date">
                        Date
                    </label>

                    <input
                        id="date"
                        name="date"
                        type="date"
                        value="{{ date }}"
                        required
                    >

                </div>

                <div class="row">

                    <div class="field">

                        <label for="time_preference">
                            Time
                        </label>

                        <select
                            id="time_preference"
                            name="time_preference"
                        >

                            <option
                                value="morning"
                                {% if time_preference == "morning" %}
                                selected
                                {% endif %}
                            >
                                Morning
                            </option>

                            <option
                                value="afternoon"
                                {% if time_preference == "afternoon" %}
                                selected
                                {% endif %}
                            >
                                Afternoon
                            </option>

                            <option
                                value="evening"
                                {% if time_preference == "evening" %}
                                selected
                                {% endif %}
                            >
                                Evening
                            </option>

                        </select>

                    </div>

                    <div class="field">

                        <label for="people">
                            People
                        </label>

                        <input
                            id="people"
                            name="people"
                            type="number"
                            min="1"
                            max="20"
                            value="{{ people }}"
                            required
                        >

                    </div>

                </div>

                <div class="actions">

                    <button
                        class="manual"
                        type="button"
                    >
                        Search manually
                    </button>

                    <div class="divider">
                        or
                    </div>

                    <button
                        class="smart"
                        id="smart-button"
                        type="submit"
                    >
                        ✨ Smart Mode
                    </button>

                </div>

            </form>

            <div
                class="loading-state"
                id="loading"
            >

                <div class="spinner"></div>

                <strong>Smart Mode is searching...</strong>

                <div style="margin-top: 4px; font-size: 13px;">
                    The agent is navigating the website and comparing tours.
                </div>

            </div>


            {% if result %}

            <div class="result">

                <div class="result-header">

                    <div class="result-title">
                        Smart Mode found a recommendation
                    </div>

                    <div class="badge">
                        AI powered
                    </div>

                </div>


                <div class="recommendation">

                    <div class="recommendation-top">

                        <div class="recommended-label">
                            Recommended tour
                        </div>

                        <div class="tour-name">
                            {{ tour_name }}
                        </div>

                        <div class="details">

                            <div class="detail">

                                <div class="detail-label">
                                    Date
                                </div>

                                <div class="detail-value">
                                    {{ display_date }}
                                </div>

                            </div>

                            <div class="detail">

                                <div class="detail-label">
                                    Time
                                </div>

                                <div class="detail-value">
                                    {{ time_preference|capitalize }}
                                </div>

                            </div>

                            <div class="detail">

                                <div class="detail-label">
                                    People
                                </div>

                                <div class="detail-value">
                                    {{ people }}
                                </div>

                            </div>

                            <div class="detail">

                                <div class="detail-label">
                                    Source
                                </div>

                                <div class="detail-value">
                                    GuruWalk
                                </div>

                            </div>

                        </div>

                    </div>


                    <div class="recommendation-actions">

                        <a
                            class="secondary-button"
                            href="{{ tour_url }}"
                            target="_blank"
                        >
                            View this tour
                        </a>

                        <a
                            class="primary-button"
                            href="{{ tour_url }}"
                            target="_blank"
                        >
                            Book this tour
                        </a>

                    </div>

                </div>


                <details class="agent-output">

                    <summary>
                        View the agent's full result
                    </summary>

                    <div style="margin-top: 12px;">
                        {{ result|safe }}
                    </div>

                </details>

            </div>

            {% endif %}


            {% if error %}

            <div class="error">
                {{ error }}
            </div>

            {% endif %}

        </div>

    </div>

</div>


<script>

    const form = document.getElementById("smart-form");
    const button = document.getElementById("smart-button");
    const loading = document.getElementById("loading");

    form.addEventListener("submit", function () {

        button.disabled = true;
        button.textContent = "✨ Smart Mode is searching...";

        loading.classList.add("visible");

    });

</script>

</body>
</html>
"""


def format_date(date_string):
    if not date_string:
        return ""

    try:
        date = datetime.strptime(
            date_string,
            "%Y-%m-%d"
        )

        return date.strftime(
            "%A, %B %d, %Y"
        ).replace(" 0", " ")

    except ValueError:
        return date_string


def extract_tour_name(answer):
    """
    Try to extract a useful tour name from the agent response.

    We ask the agent to put the recommended tour name on its own line.
    If that format is not followed, we fall back to the first
    meaningful line of the response.
    """

    lines = [
        line.strip()
        for line in answer.splitlines()
        if line.strip()
    ]

    for line in lines:

        cleaned = re.sub(
            r"^[#*\-\d\.\)\s]+",
            "",
            line
        ).strip()

        lower = cleaned.lower()

        if lower.startswith("tour name:"):
            return cleaned.split(":", 1)[1].strip()

        if lower.startswith("recommended tour:"):
            return cleaned.split(":", 1)[1].strip()

    for line in lines:

        cleaned = re.sub(
            r"^[#*\-\d\.\)\s]+",
            "",
            line
        ).strip()

        if len(cleaned) > 10 and len(cleaned) < 120:

            excluded = [
                "here are",
                "i recommend",
                "recommendation",
                "tour name",
                "time:",
                "rating:",
                "meeting point:",
                "booking url:",
            ]

            if not any(
                cleaned.lower().startswith(item)
                for item in excluded
            ):
                return cleaned

    return "Recommended walking tour"


@app.route("/", methods=["GET", "POST"])
def index():

    destination = request.form.get(
        "destination",
        "Barcelona"
    )

    date = request.form.get(
        "date",
        ""
    )

    time_preference = request.form.get(
        "time_preference",
        "morning"
    )

    people = request.form.get(
        "people",
        "2"
    )

    result = None
    error = None
    tour_name = "Recommended walking tour"
    tour_url = "https://www.guruwalk.com/"

    if request.method == "POST":

        task = f"""
Go to guruwalk.com and find a free walking tour in {destination}
for {date} in the {time_preference}.

Find options suitable for {people} people.
Compare at least two options and recommend the best one.

Please return the recommendation clearly using this format:

Tour name: [exact name of the recommended tour]
Time: [tour time]
Rating: [rating if available]
Meeting point: [meeting point if available]
Booking URL: [URL of the recommended tour]

Then briefly explain why you recommend this option.
"""

        try:

            agent_result = client.run_session(
                agent="h/web-surfer-flash",
                messages=task,
            )

            raw_answer = agent_result.answer

            result = (
                html.escape(raw_answer)
                .replace("\n", "<br>")
            )

            tour_name = extract_tour_name(
                raw_answer
            )

            # Try to find the booking URL returned by the agent.
            urls = re.findall(
                r"https?://[^\s<>\"']+",
                raw_answer
            )

            guruwalk_urls = [
                url.rstrip(".,)")
                for url in urls
                if "guruwalk.com" in url.lower()
            ]

            if guruwalk_urls:
                tour_url = guruwalk_urls[0]

        except Exception as e:

            error = (
                "The agent could not complete the search. "
                f"{html.escape(str(e))}"
            )

    return render_template_string(
        HTML,
        destination=destination,
        date=date,
        display_date=format_date(date),
        time_preference=time_preference,
        people=people,
        result=result,
        error=error,
        tour_name=tour_name,
        tour_url=tour_url,
    )


if __name__ == "__main__":
    app.run(debug=True)