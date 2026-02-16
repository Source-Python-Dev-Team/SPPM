window.onload = function(){
    console.log('create')
    const pathStrSplit = getPathSplit(window.location.pathname);
    const projectType = pathStrSplit[0];
    if (projectType === 'plugins' || projectType === 'packages') {
        if (pathStrSplit[1]) {
            const projectSlug = pathStrSplit[1];
            if (projectSlug === "create") {
                buildCreateForm(projectType);
            }
        } else {
            showListView(projectType);
        }
    }
};

async function buildCreateForm(projectType) {
    const urlPath = '/api/' + projectType + '/projects/';

    const res = await fetch(urlPath, { method: "OPTIONS" })
    const data = await res.json();
    if (!data.actions || !data.actions.POST) {
        showNotAuthenticatedMessage(projectType);
        return;
    }

    document.getElementById("create-form-view").style.display = "block";
    const singProjectType = projectType.slice(0, -1);
    document.getElementById("create-form-title").textContent = "Create " + singProjectType;

    const form = document.getElementById("dynamic-create-form");
    const fields = Object.entries(data.actions.POST).filter(([name, meta]) => !meta.read_only);
    fields.forEach(([fieldName, meta]) => {
        const fieldElement = buildField(fieldName, meta);
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
        const postRes = await fetch(urlPath, {
            method: "POST",
            headers: {
                "X-CSRFToken": csrftoken
            },
            body: formData
        });

        if (postRes.status === 201) {
            const data = await postRes.json();
            const slug = data.slug;
            console.log(`/${projectType}/${slug}`);
            window.location.href = `/${projectType}/${slug}`;
            return;
        }
        handleCreateError(form, postRes);
    });
}

function buildField(fieldName, meta, parentName = null) {
  const fullName = parentName ? `${parentName}.${fieldName}` : fieldName;

  // Handle nested objects
  if (meta.children) {
    const fieldset = document.createElement("fieldset");

    const legend = document.createElement("legend");
    legend.textContent = meta.label || fieldName;
    fieldset.appendChild(legend);

    Object.entries(meta.children).forEach(([childName, childMeta]) => {
      const childField = buildField(childName, childMeta, fullName);
      fieldset.appendChild(childField);
    });

    return fieldset;
  }

  // Handle primitive fields
  const wrapper = document.createElement("div");
  wrapper.classList.add("form-field");

  const label = document.createElement("label");
  label.textContent = meta.label || fieldName;
  label.setAttribute("for", fullName);

  if (meta.type === "string" && isLongText(meta)) {
      input = document.createElement("textarea");
      input.rows = 6;
      input.cols = 50;
  } else {
      input = document.createElement("input");
      input.type = "text";
  }
  input.name = fullName;
  input.id = fullName;

  switch (meta.type) {
    case "integer":
      input.type = "number";
      break;
    case "boolean":
      input.type = "checkbox";
      break;
    case "image upload":
      input.type = "file";
      input.accept = "image/*"
      break;
    case "file upload":
      input.type = "file";
      input.accept = ".zip"
      break;
    default:
      input.type = "text";
}

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
