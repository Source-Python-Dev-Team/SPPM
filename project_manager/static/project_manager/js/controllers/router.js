window.onload = function(){
    console.log(window.location.pathname);
    const urlSearchParams = new URLSearchParams(window.location.search);
    const params = Object.fromEntries(urlSearchParams.entries());
    console.log(params);
    const originalPath = window.location.pathname;
    const trimmedPath = originalPath.slice(1, originalPath.length - 1);
    console.log(trimmedPath);
    const pathStrSplit = trimmedPath.split("/");
    console.log(pathStrSplit);
    const basePath = pathStrSplit[0];
    if (basePath === 'plugins' || basePath === 'packages'){
        const baseUrlPath = '/api/' + basePath
        const baseProjectUrlPath = baseUrlPath + '/projects/'
        if (pathStrSplit.length === 1){
            async function getListData(){
                let response = await fetch(baseProjectUrlPath);
                if (response.status === 200) {
                    let data = await response.json();
                }
            }
        } else if (pathStrSplit.length === 2){
            const projectName = pathStrSplit[1];
            const urlPath = baseProjectUrlPath + projectName
            async function getData(){
                let response = await fetch(urlPath);
                if (response.status === 200) {
                    let data = await response.json();
                    document.getElementById('name').textContent = data.name;
                    document.getElementById('owner').textContent = data.owner.username;
                    document.getElementById('created').textContent = data.created.locale;
                    document.getElementById('configuration').textContent = data.configuration;
                    document.getElementById('description').textContent = data.description;
                    document.getElementById('synopsis').textContent = data.synopsis;
                    document.getElementById('logo').textContent = data.logo;
                    document.getElementById('video').textContent = data.video;
                } else {
                    const projectType = basePath === 'plugins' ? 'Plugin' : 'Package'
                    document.getElementById('error_msg').textContent = projectType + ' ' + projectName + ' ' + 'not found'
                }
            }
            // export let project = getData();
            getData().then();
        }
    }
};
