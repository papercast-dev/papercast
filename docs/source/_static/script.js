function removeLineComments(text) {
    const lines = text.split('\n');
    const uncommentedLines = lines.filter(line => !line.trim().startsWith('//'));
    return uncommentedLines.join('\n');
}

async function fetchPlugins() {
    const repoUrl = "https://raw.githubusercontent.com/papercast-dev/papercast-community/main/plugins.jsonc";
    const response = await fetch(repoUrl, { cache: 'no-cache' });
    const jsoncContent = await response.text();
    const uncommentedContent = removeLineComments(jsoncContent);
    console.log(uncommentedContent);
    const plugins = JSON.parse(uncommentedContent);
    console.log(plugins);
    return plugins;
}

function createBox(name, contrib, repo) {
    const container = document.createElement('div');
    container.classList.add('container');

    const middleSection = document.createElement('a');
    middleSection.classList.add('section', 'middle-section');

    if (contrib.icon) {
        console.log(contrib.icon);
        const icon = document.createElement('img');
        icon.classList.add('plugin-icon');
        icon.src = contrib.icon;
        middleSection.appendChild(icon);
    }

    else {
        console.log('no icon');
    }

    const pluginName = document.createElement('div');
    pluginName.classList.add('plugin-name');
    // Get the last part of the name
    pluginName.textContent = name.split('.').slice(-1)[0];

    middleSection.appendChild(pluginName);
    if (contrib.short_description) {
        const pluginDescription = document.createElement('div');
        pluginDescription.classList.add('plugin-description');
        pluginDescription.textContent = contrib.short_description;
        middleSection.appendChild(pluginDescription);
    }
    // Make the middle section a link if the plugin has a website
    if (repo) {
        middleSection.href = "https://github.com/" + repo;
    }
    container.appendChild(middleSection);


    // if the name doesn't include "types" 
    if (!name.includes('types')) {
        const IOSection = document.createElement('div');
        IOSection.classList.add('io-section');

        const inputSection = document.createElement('div');
        inputSection.classList.add('section', 'input-section');


        if (contrib.input_types) {
            const inputHeader = document.createElement('div');
            inputHeader.classList.add('input-header');
            inputHeader.textContent = "Input";
            inputSection.appendChild(inputHeader);
            for (const [key, value] of Object.entries(contrib.input_types)) {
                const subdivision = document.createElement('div');
                subdivision.classList.add('subdivision');
                subdivision.classList.add('input-subdivision');
                subdivision.textContent = key;
                inputSection.appendChild(subdivision);
            }
        }

        IOSection.appendChild(inputSection);

        const outputSection = document.createElement('div');
        outputSection.classList.add('section', 'output-section');


        if (contrib.output_types) {
            const outputHeader = document.createElement('div');
            outputHeader.classList.add('output-header');
            outputHeader.textContent = "Output";
            outputSection.appendChild(outputHeader);
            for (const [key, value] of Object.entries(contrib.output_types)) {
                const subdivision = document.createElement('div');
                subdivision.classList.add('subdivision');
                subdivision.classList.add('output-subdivision');
                // subdivision.textContent = key + ":" + value.replace('papercast.types.', '');
                subdivision.textContent = key;
                outputSection.appendChild(subdivision);
            }
        }
        IOSection.appendChild(outputSection);

        container.appendChild(IOSection);

    }

    return container;
}

async function init() {
    const pluginsContainerProcessors = document.getElementById('plugins-container-processors');
    const pluginsContainerSubscribers = document.getElementById('plugins-container-subscribers');
    const pluginsContainerPublishers = document.getElementById('plugins-container-publishers');
    const pluginsContainerTypes = document.getElementById('plugins-container-types');

    const plugins = await fetchPlugins();

    plugins.forEach(plugin => {
        // Check if has a .contributes property
        if (plugin.contributes) {
            for (const [key, value] of Object.entries(plugin.contributes)) {
                const box = createBox(key, value, plugin.repo);
                console.log(value)
                if (key.includes('processor')) pluginsContainerProcessors.appendChild(box);
                else if (key.includes('subscribers')) pluginsContainerSubscribers.appendChild(box);
                else if (key.includes('publishers')) pluginsContainerPublishers.appendChild(box);
                else if (key.includes('types')) pluginsContainerTypes.appendChild(box);

            }
        }
    });
}

init();