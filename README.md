# Smart Mode Walking Tour Finder

A small Flask demo showing how to integrate H's Computer Use Agents into an existing application.

The app lets users enter a destination, date, time preference, and number of people. Smart Mode turns those inputs into a task and uses the h agent to search GuruWalk and recommend a suitable tour.

## Tutorial

See the full tutorial:

[Build a Smart Mode into Your Web App with H's Computer Use Agents](https://app.notion.com/p/Build-a-Smart-Mode-into-Your-Web-App-with-H-s-Computer-Use-Agents-3d052e328c2c80feb5d5dc18418ec7b0)

## Setup

Install the dependencies:

```bash
pip install -r requirements.txt
```

Set your H API key:

```bash
export HAI_API_KEY="your-api-key"
```

Then run the application:

```bash
python app.py
```

Open the local URL shown in the terminal.

## Notes

The `Book this tour` button takes the user to the GuruWalk website, where they can review the tour and complete the booking themselves.
