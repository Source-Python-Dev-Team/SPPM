window.onload = function(){
    console.log('update')
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
};
