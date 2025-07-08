# webhook-repo

This repository contains the Flask application that acts as a webhook receiver for GitHub events
(Push, Pull Request, Merge) from the `action-repo`. It stores the event data in MongoDB and provides
an API endpoint for a UI to poll and display the latest activity.

## Setup and Running


**ENV file Structure**

MONGO_URI=mongodb://localhost:27017/ # Default local MongoDB URI
DB_NAME=github_webhooks
COLLECTION_NAME=events

**Prerequisites:**

- Python 3.x
- MongoDB Community Server (running locally or accessible via `MONGO_URI`)
- Git
- Ngrok (for local testing with GitHub webhooks)

**1. Clone the repository:**

```bash
git clone [https://github.com/YOUR_GITHUB_USERNAME/webhook-repo.git](https://github.com/YOUR_GITHUB_USERNAME/webhook-repo.git)
cd webhook-repo
