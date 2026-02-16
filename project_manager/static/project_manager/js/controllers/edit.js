window.onload = function(){
    console.log('edit')
    const pathStrSplit = getPathSplit(window.location.pathname);
    const projectType = pathStrSplit[0];
    if (projectType === 'plugins' || projectType === 'packages') {
        if (pathStrSplit[1]) {
            const projectSlug = pathStrSplit[1];
            buildEditForm(projectType, projectSlug);
        }
    }
};

async function buildEditForm(projectType, projectSlug) {
    const urlPath = '/api/' + projectType + '/projects/' + projectSlug + '/';

    const optionsRes = await fetch(urlPath, { method: "OPTIONS" })
    const optionsData = await optionsRes.json();

    if (!optionsData.actions || !optionsData.actions.PATCH) {
        showNotAuthenticatedMessage(projectType);
        return;
    }

    const getRes = await fetch(urlPath)
    const existingData = await getRes.json();

    console.log(optionsData.actions);

    document.getElementById("edit-form-view").style.display = "block";
    const singProjectType = projectType.slice(0, -1);
    document.getElementById("edit-form-title").textContent = "Edit " + singProjectType;

    const form = document.getElementById("dynamic-edit-form");
    const fields = Object.entries(optionsData.actions.PATCH).filter(([name, meta]) => !meta.read_only);
    fields.forEach(([fieldName, meta]) => {
        const fieldElement = buildFieldFromExisting(fieldName, meta, existingData[fieldName]);
        form.appendChild(fieldElement);
    });

    const submit = document.createElement("button");
    submit.type = "submit";
    submit.textContent = "Submit";
    form.appendChild(submit);

    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        const csrftoken = getCookie("csrftoken");
        const formData = buildFormData(form, fields);
        console.log(formData);
        console.log(urlPath);
        const postRes = await fetch(urlPath, {
            method: "PATCH",
            headers: {
                "X-CSRFToken": csrftoken
            },
            body: formData
        });

        if (postRes.status === 200) {
            console.log(`/${projectType}/${slug}`);
            window.location.href = `/${projectType}/${projectSlug}`;
            return;
        }
        handleCreateError(form, postRes);
    });
}

function buildFieldFromExisting(fieldName, meta, value) {
  // Handle primitive fields
  const wrapper = document.createElement("div");
  wrapper.classList.add("form-field");

  const label = document.createElement("label");
  label.textContent = meta.label || fieldName;

  let input;

  if (meta.type === "string" && isLongText(meta)) {
      input = document.createElement("textarea");
      input.rows = 6;
      input.cols = 50;
  } else {
      input = document.createElement("input");
      input.type = "text";
  }

  switch (meta.type) {
    case "integer":
      input.type = "number";
      input.value = value || 0;
      break;
    case "boolean":
      input.type = "checkbox";
      input.checked = Boolean(value);
      break;
    case "image upload": {
      input.type = "file";
      input.accept = "image/*";

      // Show existing image if present
      if (value) {
        const preview = document.createElement("img");
        preview.src = value;
        preview.classList.add("image-preview");
        wrapper.appendChild(preview);
      }
      break;
    }
    case "file upload": {
      input.type = "file";
      input.accept = ".zip";

      // Show existing file link if present
      if (value) {
        const link = document.createElement("a");
        link.href = value;
        link.textContent = "Current file";
        link.target = "_blank";
        wrapper.appendChild(link);
      }
      break;
    }
    default:
      input.type = "text";
      input.value = value || "";
  }
  input.name = fieldName;

  if (meta.required) {
      input.required = true;
      label.classList.add("required-asterisk");
  }

  wrapper.appendChild(label);
  if (meta.help_text) {
      const help = document.createElement("small");
      help.textContent = meta.help_text;
      help.classList.add("help-text");
      wrapper.appendChild(help);
  }
  wrapper.appendChild(input);

  return wrapper;
}

function buildFormData(form, fields, formData = new FormData(), prefix = "") {
    fields.forEach(([fieldName, meta]) => {
        const fullName = prefix ? `${prefix}.${fieldName}` : fieldName;

        if (meta.children) {
            buildFormData(form, Object.entries(meta.children), formData, fullName);
            return;
        }

        const input = form.querySelector(`[name="${fullName}"]`);
        if (!input) return;

        if (meta.type === "boolean") {
            formData.append(fullName, input.checked);
        } else if (meta.type === "file upload" || meta.type === "image upload") {
            if (input.files.length > 0) {
                formData.append(fullName, input.files[0] || null);
            }
        } else {
            formData.append(fullName, input.value);
        }
    });

    return formData;
}

function buildFormDataForPatch(form, fields, existingValue) {
    const formData = new FormData();
    fields.forEach(([fieldName, meta]) => {

        const input = form.querySelector(`[name="${fieldName}"]`);
        if (!input) return;

        if (input.type === "file") {
            if (input.files.length > 0) {
                formData.append(fieldName, input.files[0]);
            }
            return;
        }

        console.log(fieldName)
    });

    return formData;
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
