function isLongText(meta) {
    return !!(meta.max_length && meta.max_length > 200);
}

function showNotAuthenticatedMessage(projectType) {
  const singProjectType = projectType.slice(0, -1);
  const formView = document.getElementById("form-view");
  formView.style.display = "block";
  formView.innerHTML = `
    <div class="auth-warning">
      <h2>You must be logged in to create a new ${singProjectType}.</h2>
      <p>Please log in and try again.</p>
    </div>
  `;
}

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

async function handleCreateError(form, response) {
    // Try to parse error details (DRF usually returns JSON)
    let errorText = "There was a problem creating your project.";

    try {
        const err = await response.json();
        errorText = Object.values(err).flat().join(" ");
    } catch (e) {
        // If JSON parsing fails, keep default message
    }

    // Clear the form
    form.reset();

    // Insert an error message at the top
    const msg = document.createElement("div");
    msg.classList.add("form-error-message");
    msg.textContent = errorText;

    form.prepend(msg);
}
