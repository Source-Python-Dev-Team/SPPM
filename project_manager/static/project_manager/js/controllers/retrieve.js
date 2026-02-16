window.onload = function(){
    const urlSearchParams = window.location.search;
    const pathStrSplit = getPathSplit(window.location.pathname);
    const projectType = pathStrSplit[0];
    let urlPath = "/api/" + projectType + "/projects/";
    let projectSlug = pathStrSplit[1];
    if (pathStrSplit[2] === "sub-plugins" && projectType === "plugins") {
        urlPath = "/api/sub-plugins/projects/" + projectSlug + "/";
        projectSlug = pathStrSplit[3];
    }
    if (projectSlug) {
        urlPath = urlPath + projectSlug + "/";
        showDetailView(urlPath);
    } else {
        showListView(urlPath, urlSearchParams);
    }
};

function showListView(urlPath, urlSearchParams) {
    document.getElementById("list-view").style.display = "block";
    const fullApiUrl = `${urlPath}${urlSearchParams}`
    fetch(fullApiUrl)
        .then(res => res.json())
        .then(data => {
            const container = document.getElementById("project-list");
            const template = document.getElementById("project-item-template");
            container.innerHTML = "";
            data.results.forEach((item) => {
                const clone = template.content.cloneNode(true);
                const link = clone.querySelector(".project-link");
                link.href = item.slug;
                clone.querySelector(".project-name").textContent = item.name;
                clone.querySelector(".project-version").textContent = ` - ${item.current_release.version}`;
                if (item.video_embed_html) {
                    const videoContainer = clone.querySelector(".project-video");
                    videoContainer.innerHTML = item.video_embed_html;
                    videoContainer.style.display = "block";
                } else if (item.logo) {
                    const logoEl = clone.querySelector(".project-logo");
                    logoEl.src = item.logo;
                    logoEl.style.display = "block";
                } else {
                    const fallbackEl = clone.querySelector(".project-fallback");
                    fallbackEl.style.display = "block";
                }
                container.appendChild(clone);
            })
        })
}

function showDetailView(urlPath) {
    document.getElementById("detail-view").style.display = "block";
    fetch(urlPath)
        .then(res => res.json())
        .then(data => {
            document.getElementById("project-name").textContent = data.name;
            document.getElementById("project-owner").textContent = data.owner.username;
            document.getElementById("project-downloads").textContent = data.total_downloads;
            document.getElementById("project-synopsis").textContent = data.synopsis;
            document.getElementById("project-version").textContent = data.current_release.version;
        })
}
