window.onload = function(){
    console.log('delete')
    const pathStrSplit = getPathSplit(window.location.pathname);
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

