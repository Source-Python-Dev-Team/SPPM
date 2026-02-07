window.onload = function(){
    console.log('delete')
    const urlSearchParams = new URLSearchParams(window.location.search);
    const params = Object.fromEntries(urlSearchParams.entries());
    let originalPath = window.location.pathname;
    if (originalPath.startsWith("/")) {
        originalPath = originalPath.slice(1);
    }
    if (originalPath.endsWith("/")) {
        originalPath = originalPath.slice(0, -1);
    }
    const pathStrSplit = originalPath.split("/");
    const projectType = pathStrSplit[0];
    if (projectType === 'plugins' || projectType === 'packages') {
        if (pathStrSplit[1]) {
            const projectSlug = pathStrSplit[1];
            if (projectSlug === "create") {
                buildCreateForm(projectType);
            } else {
                const projectAction = pathStrSplit[2];
                if (!projectAction) {
                    showDetailView(projectType, projectSlug);
                } else if (projectAction === "edit") {
                    buildEditForm(projectType, projectSlug);
                // } else if (projectAction === "update") {
                //     buildUpdateForm(projectAction, projectSlug);
                }
            }
        } else {
            showListView(projectType);
        }
    }
};

