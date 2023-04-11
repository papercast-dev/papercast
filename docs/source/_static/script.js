function removeLineComments(text) {
    const lines = text.split('\n');
    const uncommentedLines = lines.filter(line => !line.trim().startsWith('//'));
    return uncommentedLines.join('\n');
}

async function fetchPlugins() {
    const repoUrl = "https://raw.githubusercontent.com/papercast-dev/papercast-community/main/plugins.jsonc";
    const response = await fetch(repoUrl);
    const jsoncContent = await response.text();
    const uncommentedContent = removeLineComments(jsoncContent);
    console.log(uncommentedContent);
    const plugins = JSON.parse(uncommentedContent);
    console.log(plugins);
    return plugins;
}

function createBox(plugin, type) {
    const container = document.createElement('div');
    container.classList.add('container');

    const inputSection = document.createElement('div');
    inputSection.classList.add('section', 'input-section');
    // plugin.inputs.forEach(input => {
    //     const subdivision = document.createElement('div');
    //     subdivision.classList.add('subdivision');
    //     subdivision.textContent = input;
    //     inputSection.appendChild(subdivision);
    // });
    container.appendChild(inputSection);

    const middleSection = document.createElement('a');
    middleSection.classList.add('section', 'middle-section');
    if (plugin.icon) {
        console.log(plugin.icon);
        const icon = document.createElement('img');
        icon.classList.add('plugin-icon');
        icon.src = plugin.icon;
        middleSection.appendChild(icon);
    }
    else {
        console.log('no icon');
    }
    const pluginName = document.createElement('div');
    pluginName.classList.add('plugin-name');
    pluginName.textContent = plugin.name;
    middleSection.appendChild(pluginName);
    // Make the middle section a link if the plugin has a website
    if (plugin.repo) {
        middleSection.href = "https://github.com/" + plugin.repo;
    }
    container.appendChild(middleSection);



    if ((type === 'processor') || (type === 'collector')) {
        const outputSection = document.createElement('div');
        outputSection.classList.add('section', 'output-section');
        // plugin.outputs.forEach(output => {
        //     const subdivision = document.createElement('div');
        //     subdivision.classList.add('subdivision');
        //     subdivision.textContent = output;
        //     outputSection.appendChild(subdivision);
        // });
        container.appendChild(outputSection);
    }

    return container;
}

async function init() {
    const pluginsContainerProcessors = document.getElementById('plugins-container-processors');
    const pluginsContainerCollectors = document.getElementById('plugins-container-collectors');
    const pluginsContainerPublishers = document.getElementById('plugins-container-publishers');

    const plugins = await fetchPlugins();

    plugins.forEach(plugin => {
        const box = createBox(plugin, plugin.type);
        if (plugin.type === 'processor') pluginsContainerProcessors.appendChild(box);
        else if (plugin.type === 'collector') pluginsContainerCollectors.appendChild(box);
        else if (plugin.type === 'publisher') pluginsContainerPublishers.appendChild(box);
    });
}

init();