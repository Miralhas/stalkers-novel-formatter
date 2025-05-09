# Stalkers Novel Formatter
> Collection of scripts that clean, extract and format a Novel. 

## Format Novel - Script
This script formats given root folder _(folder generated by the lightnovel-crawler script)_ into a single json that follows the Stalkers API standards.

#### Options Args:
```powershell
--root Path # Path to the folder generated by the lightnovel-crawler script
```

#### Example:
> The following example format, cleans and extract all the novel informations from the provided root folder
```powershell
python .\format_novel.py --root "C:\Users\bob\Desktop\NovelOutput\AdventOfTheThreeCalamities" # --root is the folder generated by the lightnovel-crawler script
```

_Output:_
###### This output contains all novel information and chapters. It's stored at the _./output_ folder and later will be sent to the Stalkers API through a http post method
```json
{
    "title": "advent of the three calamities",
    "author": "Entrail_JI",
    "description": "<p>[From the Author of Author&#39;s POV...]\n<br/>\n<br/>Emotions are like a drug to us.\n<br/>\n<br/>The more we have them, the more we become addicted\n<br/>",
    "categories": [
        "action",
        "comedy",
        "fantasy",
        "romance"
    ],
    "tags": [
        "fantasy",
        "no-harem",
        "romance",
        "academy",
        "comedy",
        "action",
        "transmigration",
        "genius",
        "levelup",
        "sliceoflife",
        "videogame"
    ],
    "chapters": [
        {
            "number": 1,
            "id": 1,
            "title": "Chapter 1: Prologue [1]",
            "body": "<h1>Chapter 1: Prologue [1]</h1><p>Chapter 1: Prologue [1]</p><p>Emotions.</p><p>A strong feeling (reaction) deriving from one&#39;s circumstances, mood, or relationship with others.</p><p>Inever fully understood them.</p><p>They weren&#39;t foreign to me—Anger, Sadness, Fear, Guilt...—I&#39;ve experienced them all. Plenty of times before.</p><p>As humans, we were inherently designed to feel them.</p>..."
        },
        {
           "number": 2,
            "id": 2,
            "title": "Chapter 2: Julien D. Evenus [1]",
            "body": "<h1>Chapter 2: Julien D. Evenus [1]</h1><p>Chapter 2: Julien D. Evenus [1]</p><p><i>&#39;Uh... I&#39;m still alive?&#39;</i></p><p>There was no way. But... I was starting to doubt it. That was despite feeling certain that I had drawn my last breath.</p>..."
        }
    ]
}
```


***

## Get Novel Metadata - Script
This script extracts some required metadatas of a given novel.

#### Options Args:
```powershell
--root PATH # Path to the folder generated by the lightnovel-crawler script
--source STR # Source from which the metadata will be extracted. Available Sources: ["WebnovelDotCom", "LightnovelUpdates"]
--metadata-uri STR # Uri for the novel from the selected source website.
```

#### Example:
> The following example extracts metadata from https://www.webnovel.com/book/advent-of-the-three-calamities_28449030200102805
```powershell
python .\get_novel_metadata.py --root "C:\Users\bob\Desktop\NovelOutput\AdventOfTheThreeCalamities" --source "WebnovelDotCom" --metadata-uri "advent-of-the-three-calamities_28449030200102805"
```
_Output:_
###### This output overrides the {root_folder}/meta.json file that is generated by the lightnovel-crawler script
```json
{
    "title": "advent of the three calamities",
    "author": "Entrail_JI",
    "description": "<p>[From the Author of Author&#39;s POV...]\n<br/>\n<br/>Emotions are like a drug to us.\n<br/>\n<br/>The more we experience them, the more we become addicted.\n<br/>\n<br/>The hardest part is not letting them consume us.\n<br/>\n<br/>But it&#39;s already too late for me.\n<br/>\n<br/>I&#39;ve already been swallowed whole. \n<br/>\n<br/>*** \n<br/>\n<br/>I had no knowledge of the game. \n<br/>\n<br/>I was meant to have died. \n<br/>\n<br/>And yet, I found myself in this situation. \n<br/>\n<br/>A game I had never played before. A character I was unfamiliar with, and... A world that seemed to want to swallow me whole with every move I made. \n<br/>\n<br/>What the hell is going on?\n<br/>\n<br/>...and who am I?\n<br/>\n<br/>***\n<br/>Discord : https://discord.gg/PEbN7fc2ww</p>",
    "categories": [
        "action",
        "comedy",
        "fantasy",
        "romance"
    ],
    "tags": [
        "fantasy",
        "no-harem",
        "romance",
        "academy",
        "comedy",
        "action",
        "transmigration",
        "genius",
        "levelup",
        "sliceoflife",
        "videogame"
    ]
}
```