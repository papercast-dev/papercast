# Contributing

## To contribute a plugin...

... Follow these steps:

1. Clone/fork the template at https://github.com/papercast-dev/papercast-plugin-template

2. Write your plugin

3. Publish your plugin to a github repo

4. Fork the papercast-community repo at https://github.com/papercast-dev/papercast-community

5. Add an entry to the plugins.jsoc file with your plugin specs. 

  - Your plugin can contribue multiple classes, as well as custom types.
  
  Here's an example from the ZoteroSubscriber plugin:

```json
    {
        "id": "papercast-zotero-subscriber", // plugin identifier, not currently used but may be used in docs
        "name": "Zotero", // Name for the plugin, not currently used but may be used in docs
        "author": "papercast-dev", // Your name
        "description": "Trigger pipelines when new papers are added to Zotero", // Description for the overall plugin
        "type": "collector", // DEPRECATED
        "repo": "papercast-dev/papercast-zotero-subscriber", // the github repo where your plugin is published
        "contributes": {
            "papercast.types.ZoteroOutput": {}, // custom types that your plugin contributes
            "papercast.subscribers.ZoteroSubscriber": { // custom classes (subscribers, processors, publishers) that your plugin contributes
                "icon": "https://raw.githubusercontent.com/papercast-dev/papercast-community/main/assets/img/zotero.png",  // link to an icon for your plugin
                "short_description": "Trigger pipelines when new papers are added to Zotero", // Description for the class, appears in the docs
                "output_types": {
                    "zotero_output": "papercast.types.ZoteroOutput" // input and output types
                }
            }
        }
    },
```

6. Submit a pull request to the papercast-community repo
