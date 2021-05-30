//swaps out all inputs where [data-custom-type="tag"]
generateTagInputs();

//Common choices for guessing
var commonChoices;
var dictionary;

//Renders custom field based on input[data-custom-type='tag']
function generateTagInputs() {

    //Records all inputs that need to be swapped
    fields = document.querySelectorAll("select[data-custom-type='tag']");

    for (let i = 0; i < fields.length; i++) {

        //Records all relevant input props
        const field = fields[i];
        const id = field.id;
        const className = field.className;
        const name = field.name;
        const required = field.required;

        commonChoices = [];
        [...field.options].map(opt => {
            if (!commonChoices.includes(opt.innerHTML)) {
                commonChoices.push(opt.innerHTML);
            }
        });

        const chosenChoices = [];
        [...field.options].map(opt => {
            if (!chosenChoices.includes(opt.innerHTML) && opt.selected) {
                chosenChoices.push(opt.innerHTML);
            }
        });

        //Renders custom tag input with given props in place of input
        field.outerHTML = `
        <div class="tag-container ">
            <div class="tag-field ${className}" data-tags-display="${id}">
            </div>
            <div data-tags="${id}" data-focus-index="-1" class="tag-dropdown"></div>
            <select style="display: none;" data-tags-value="${id}"} multiple>
            </select>
            <select style="display: none;" name="${name}" id="${id}" ${required ? "required" : ""} multiple>
            </select>
        </div>
        `
        renderList(chosenChoices, id);
        document.querySelector(`[data-tags-display="${id}"]`).innerHTML += `
        <input type="text" class="tag-input" data-tags-input="${id}" onfocus="inputFocus(event, 'focus')"
            onblur="inputFocus(event, 'blur')" autocomplete="off" max="24">
        `
        changeSelectValue(chosenChoices, id);
    }
}

//Implements field interactions
const tagFields = document.getElementsByClassName("tag-field");
for (let i = 0; i < tagFields.length; i++) {
    tagFields[i].addEventListener("input", (e) => { parseTags(e) });
    tagFields[i].addEventListener("keydown", (e) => { enterInput(e) });
    tagFields[i].addEventListener("click", (e) => { clickField(e) });
}

//Reads from input to display likely choices
function parseTags(e) {

    //Records dropdown list element
    const choiceList = document.querySelector(`[data-tags="${e.target.dataset.tagsInput}"]`);

    //Resets dropdown HTML + style to empty
    choiceList.innerHTML = "";
    choiceList.classList.remove("tag-dropdown-focus");

    //If input is not empty + does not end in \ (regex throws error if it is)
    if (e.target.value && e.target.value[e.target.value.length - 1] != "\\") {

        //Creates regex from input + a list to record predictions
        const autoTagComplete = new RegExp(e.target.value, "i");
        const autoCompleteList = [];

        //Loops through predictions
        for (let i = 0; i < commonChoices.length; i++) {

            //If input is similar to a prediction to add to dropdown
            if (autoTagComplete.test(commonChoices[i])) {

                //Records chosen items list + hidden input where actual data is recorded
                const tagDisplay = document.querySelector(`[data-tags-display="${e.target.dataset.tagsInput}"]`);
                const tagData = document.querySelector(`[data-tags-value="${e.target.dataset.tagsInput}"]`);

                //Parses existing data from hidden select
                const chosenTagsHTML = [...tagData.options]
                const chosenTags = chosenTagsHTML.length ? chosenTagsHTML.filter(opt => opt.selected).map(opt => opt.value) : [];

                //Adds prediction + its similarity to the user input (only if it isn't already there)
                if (!chosenTags.includes(commonChoices[i])) {
                    autoCompleteList.push({ value: commonChoices[i], similarity: similarity(e.target.value, commonChoices[i]) });
                }
            }
        }

        //Sort the predictions list based on similarity (more similar if it starts with user input)
        autoCompleteList.sort((a, b) => {
            if (a.value.toLowerCase().startsWith(e.target.value.toLowerCase())) a.similarity++;
            if (b.value.toLowerCase().startsWith(e.target.value.toLowerCase())) b.similarity++;
            return b.similarity - a.similarity;
        });

        //adds top 5 prediction to dropdown +  stylistically focuses dropdown
        let listLength = 0;
        for (let i = 0; i < autoCompleteList.length; i++) {
            if (listLength < 5) {
                choiceList.innerHTML += `<div data-value="${autoCompleteList[i].value}" data-index="${listLength}" tabindex="0" onkeydown="navigateChoices(event)" onblur="inputFocus(event, 'blur')" onclick="cleanInput(event)" class="dropdown-item">${autoCompleteList[i].value}</div>`;
                choiceList.classList.add("tag-dropdown-focus");
                listLength++;
            }
        }
    }
}

//Detects keystrokes to determine whether any hotkeys have been pressed
function enterInput(e) {

    //If 'enter' is pressed + input is not empty
    //Adds answer (if there is one) directly to chosen list
    if (e.keyCode == 13 && e.target.value) {

        //Records the input element + its HTML for later use
        const tagInput = document.querySelector(`[data-tags-input="${e.target.dataset.tagsInput}"]`);
        const tagInputHTML = tagInput.outerHTML;

        //Records chosen items list + hidden input where actual data is recorded
        const tagDisplay = document.querySelector(`[data-tags-display="${e.target.dataset.tagsInput}"]`);
        const tagData = document.querySelector(`[data-tags-value="${e.target.dataset.tagsInput}"]`);

        //Parses existing data from hidden select
        const chosenTagsHTML = [...tagData.options]
        const chosenTags = chosenTagsHTML.length ? chosenTagsHTML.filter(opt => opt.selected).map(opt => opt.value) : [];

        //Adds item to existing data if is not already there
        if (!chosenTags.includes(e.target.value)) {
            chosenTags.push(e.target.value);

            //If data is not empty
            if (chosenTags && chosenTags.length) {

                //Clears input field (including chosen items)
                tagDisplay.innerHTML = "";

                //Changes all " into &quot; to ensure HTML can read it + renders it into an HTML element
                renderList(chosenTags, e.target.dataset.tagsInput)

                //Adds the input back in to the field as it was + stores data in hidden select
                tagDisplay.innerHTML += tagInputHTML;
                changeSelectValue(chosenTags, e.target.dataset.tagsInput);
            }

            //If data is empty event after new item is added then reset input field
            else {
                tagDisplay.innerHTML = tagInputHTML;
                tagData.value = "";
            }

            //Records dropdown list element
            const choiceList = document.querySelector(`[data-tags="${e.target.dataset.tagsInput}"]`);

            //Resets dropdown HTML + style to empty
            choiceList.innerHTML = "";
            choiceList.classList.remove("tag-dropdown-focus");

            //Prevents tab from moving focus to next element + focuses back to input
            e.preventDefault();
            document.querySelector(`[data-tags-input="${e.target.dataset.tagsInput}"]`).focus();
        }

        //If 'backspace' is pressed + input is empty
        //Removes latest answer from list
    } else if (e.keyCode == 8 && e.target.value == "") {

        //Records the input element + its HTML for later use
        const tagInput = document.querySelector(`[data-tags-input="${e.target.dataset.tagsInput}"]`);
        const tagInputHTML = tagInput.outerHTML;

        //Records chosen items list + hidden input where actual data is recorded
        const tagDisplay = document.querySelector(`[data-tags-display="${e.target.dataset.tagsInput}"]`);
        const tagData = document.querySelector(`[data-tags-value="${e.target.dataset.tagsInput}"]`);

        //Parses existing data from hidden select
        const chosenTagsHTML = [...tagData.options]
        const chosenTags = chosenTagsHTML.length ? chosenTagsHTML.filter(opt => opt.selected).map(opt => opt.value) : [];

        //Removes last element
        chosenTags.pop();

        //Clears input field (including chosen items)
        tagDisplay.innerHTML = "";

        //If data is not empty
        if (chosenTags && chosenTags.length) {

            //Changes all " into &quot; to ensure HTML can read it + renders it into an HTML element
            renderList(chosenTags, e.target.dataset.tagsInput)
        }

        //Adds the input back in to the field as it was + stores data in hidden select
        tagDisplay.innerHTML += tagInputHTML;
        changeSelectValue(chosenTags, e.target.dataset.tagsInput);

        //Focuses back to input
        document.querySelector(`[data-tags-input="${e.target.dataset.tagsInput}"]`).focus();
    }

    //If 'tab' is pressed + input is not empty
    //Adds most similar prediction (if there is one) directly to chosen list
    else if (e.keyCode == 9 && e.target.value) {

        //Records dropdown list element
        const choiceList = document.querySelector(`[data-tags="${e.target.dataset.tagsInput}"]`);

        //Records value of most similar prediction
        const tabTagValue = choiceList.children[0] ? choiceList.children[0].dataset.value : undefined;

        //If there is a most similar prediction
        if (tabTagValue) {

            //Records the input element + its HTML for later use
            const tagInput = document.querySelector(`[data-tags-input="${e.target.dataset.tagsInput}"]`);
            const tagInputHTML = tagInput.outerHTML;

            //Records chosen items list + hidden input where actual data is recorded
            const tagDisplay = document.querySelector(`[data-tags-display="${e.target.dataset.tagsInput}"]`);
            const tagData = document.querySelector(`[data-tags-value="${e.target.dataset.tagsInput}"]`);

            //Parses existing data from hidden select
            const chosenTagsHTML = [...tagData.options]
            const chosenTags = chosenTagsHTML.length ? chosenTagsHTML.filter(opt => opt.selected).map(opt => opt.value) : [];

            //Adds item to existing data if is not already there
            if (!chosenTags.includes(tabTagValue)) {
                chosenTags.push(tabTagValue);

                //If data is not empty
                if (chosenTags && chosenTags.length) {

                    //Clears input field (including chosen items)
                    tagDisplay.innerHTML = "";

                    //Changes all " into &quot; to ensure HTML can read it + renders it into an HTML element
                    renderList(chosenTags, e.target.dataset.tagsInput)

                    //Adds the input back in to the field as it was + stores data in hidden select
                    tagDisplay.innerHTML += tagInputHTML;
                    changeSelectValue(chosenTags, e.target.dataset.tagsInput);
                }

                //If data is empty event after new item is added then reset input field
                else {
                    tagDisplay.innerHTML = tagInputHTML;
                    tagData.value = "";
                }

                //Resets dropdown HTML + style to empty
                choiceList.innerHTML = "";
                choiceList.classList.remove("tag-dropdown-focus");

                //Prevents tab from moving focus to next element + focuses back to input
                e.preventDefault();
                document.querySelector(`[data-tags-input="${e.target.dataset.tagsInput}"]`).focus();
            }
        }
    }

    //If 'down' is pressed + input is not empty
    //Selects to most similar input
    else if (e.keyCode == 40 && e.target.value) {

        //Records all predictionss of dropdown list
        const choiceList = document.querySelector(`[data-tags="${e.target.dataset.tagsInput}"]`).children;

        //Focus on the first child if it exists
        if (choiceList[0]) {
            choiceList[0].focus();
        }
    }
}

//Navigates across predictions of dropdown list
function navigateChoices(e) {

    //Records which input field the dropdown prediction belongs to
    const tag = e.target.parentElement.dataset.tags;

    //Parses the index of the dropdown child
    const index = parseInt(e.target.dataset.index);

    //If 'down' is pressed + last child is not selected
    //Focuses on next child (selects next prediction)
    if (e.keyCode == 40 && index < 4) {
        document.querySelector(`[data-tags="${tag}"] [data-index="${index + 1}"]`).focus();
    }

    //If 'up' is pressed + first child is not selected
    //Focuses on previous child (selects previous prediction)
    else if (e.keyCode == 38 && index > 0) {
        document.querySelector(`[data-tags="${tag}"] [data-index="${index - 1}"]`).focus();
    }

    //If 'up' is pressed + first child is selected
    //Focuses back to input
    else if (e.keyCode == 38 && index == 0) {
        document.querySelector(`[data-tags-input="${tag}"]`).focus();
    }

    //If 'enter' is pressed + input is not empty
    //Adds selected answer (if there is one) to chosen list
    else if (e.keyCode == 13) {

        //Records dropdown list element
        const choiceList = document.querySelector(`[data-tags="${tag}"]`);

        //Records value of selected prediction
        const tabTagValue = choiceList.children[index].dataset.value;

        //If there is a selected prediction
        if (tabTagValue) {

            //Records the input element + its HTML for later use
            const tagInput = document.querySelector(`[data-tags-input="${tag}"]`);
            const tagInputHTML = tagInput.outerHTML;

            //Records chosen items list + hidden input where actual data is recorded
            const tagDisplay = document.querySelector(`[data-tags-display="${tag}"]`);
            const tagData = document.querySelector(`[data-tags-value="${tag}"]`);

            //Parses existing data from hidden select
            const chosenTagsHTML = [...tagData.options]
            const chosenTags = chosenTagsHTML.length ? chosenTagsHTML.filter(opt => opt.selected).map(opt => opt.value) : [];

            //Adds item to existing data (it cannot be there via prediction)
            chosenTags.push(tabTagValue);

            //If data is not empty
            if (chosenTags && chosenTags.length) {

                //Clears input field (including chosen items)
                tagDisplay.innerHTML = "";

                //Changes all " into &quot; to ensure HTML can read it + renders it into an HTML element
                renderList(chosenTags, tag);

                //Adds the input back in to the field as it was + stores data in hidden select
                tagDisplay.innerHTML += tagInputHTML;
                changeSelectValue(chosenTags, tag);
            }

            //If data is empty event after new item is added then reset input field
            else {
                tagDisplay.innerHTML = tagInputHTML;
                tagData.value = "";
            }


            //Resets dropdown HTML + style to empty
            choiceList.innerHTML = "";
            choiceList.classList.remove("tag-dropdown-focus");

            //Focuses back to input
            document.querySelector(`[data-tags-input="${tag}"]`).focus();
        }
    }
}

//Adds selected answer (if there is one) to chosen list
function cleanInput(e) {

    //Records dropdown list element
    const choiceList = document.querySelector(`[data-tags="${e.target.parentElement.dataset.tags}"]`);

    //Resets dropdown style to empty
    choiceList.classList.remove("tag-dropdown-focus");

    //Records which input field the dropdown prediction belongs to
    const inputId = e.target.parentElement.dataset.tags;

    //Records the input element + its HTML for later use + clears input
    const tagInput = document.querySelector(`[data-tags-input="${e.target.parentElement.dataset.tags}"]`);
    const tagInputHTML = tagInput.outerHTML;
    tagInput.value = "";

    //Records value of selected prediction
    const tag = e.target.dataset.value;

    //Records chosen items list + hidden input where actual data is recorded
    const tagDisplay = document.querySelector(`[data-tags-display="${e.target.parentElement.dataset.tags}"]`);
    const tagData = document.querySelector(`[data-tags-value="${e.target.parentElement.dataset.tags}"]`);

    //Parses existing data from hidden select
    const chosenTagsHTML = [...tagData.options]
    const chosenTags = chosenTagsHTML.length ? chosenTagsHTML.filter(opt => opt.selected).map(opt => opt.value) : [];

    //Adds item to existing data (it cannot be there via prediction)
    chosenTags.push(tag);
    if (chosenTags && chosenTags.length) {

        //Clears input field (including chosen items)
        tagDisplay.innerHTML = "";

        //Changes all " into &quot; to ensure HTML can read it + renders it into an HTML element
        renderList(chosenTags, e.target.parentElement.dataset.tags);

        //Adds the input back in to the field as it was + stores data in hidden select
        tagDisplay.innerHTML += tagInputHTML;
        changeSelectValue(chosenTags, e.target.parentElement.dataset.tags);
    }

    //If data is empty event after new item is added then reset input field
    else {
        tagDisplay.innerHTML = tagInputHTML;
        tagData.value = "";
    }

    //Resets dropdown HTML + style to empty
    choiceList.innerHTML = "";
    choiceList.classList.remove("tag-dropdown-focus");

    //Focuses back to input
    document.querySelector(`[data-tags-input="${inputId}"]`).focus();
}

//Deletes chosen item on click
function deleteItem(e) {

    //Records the input element + its HTML + its value for later use + clears input
    const tagInput = document.querySelector(`[data-tags-input="${e.currentTarget.parentElement.dataset.tagOf}"]`);
    const tagInputHTML = tagInput.outerHTML;
    const tagInputValue = tagInput.value;

    //Records chosen items list + hidden input where actual data is recorded
    const tagDisplay = document.querySelector(`[data-tags-display="${e.currentTarget.parentElement.dataset.tagOf}"]`);
    const tagData = document.querySelector(`[data-tags-value="${e.currentTarget.parentElement.dataset.tagOf}"]`);

    //Parses existing data from hidden select
    const chosenTagsHTML = [...tagData.options]
    const chosenTags = chosenTagsHTML.length ? chosenTagsHTML.filter(opt => opt.selected).map(opt => opt.value) : [];

    //Removes selected element
    const filteredTags = chosenTags.filter(value => value != e.currentTarget.parentElement.dataset.value);

    //Clears input field (including chosen items)
    tagDisplay.innerHTML = "";

    //Checks if data is empty
    if (filteredTags && filteredTags.length) {

        //Changes all " into &quot; to ensure HTML can read it + renders it into an HTML element
        renderList(filteredTags, e.currentTarget.parentElement.dataset.tagOf);
    }

    //Adds the input and its value back in to the field as it was + stores data in hidden select
    tagDisplay.innerHTML += tagInputHTML;
    document.querySelector(`[data-tags-input="${e.currentTarget.parentElement.dataset.tagOf}"]`).value = tagInputValue;
    changeSelectValue(filteredTags, e.currentTarget.parentElement.dataset.tagOf);


    //Focuses back to input
    document.querySelector(`[data-tags-input="${e.currentTarget.parentElement.dataset.tagOf}"]`).focus();
}

//Focuses to input when the field is clicked
function clickField(e) {
    document.querySelector(`[data-tags-input="${e.currentTarget.dataset.tagsDisplay}"]`).focus();
}

//Determins focus and blur interactions of field
function inputFocus(e, state) {

    //Records chosen items list
    const tagsDisplay = document.querySelector(`[data-tags-display="${e.target.dataset.tagsInput ? e.target.dataset.tagsInput : e.target.parentElement.dataset.tags}"]`);

    //setTimeout for list disappearance + styles (to give program time to react to clicks etc.)
    setTimeout(() => {
        switch (state) {
            case "focus":

                //Adds style to field
                if (!tagsDisplay.classList.contains('tag-field-focus')) {
                    tagsDisplay.classList.add('tag-field-focus');
                }
                break;
            case "blur":

                //Checks if the new focus is a dropdown child
                let isChildFocus = false;
                if (e.target.dataset.tagsInput || e.target.parentElement) {
                    const choiceList = document.querySelector(`[data-tags="${e.target.dataset.tagsInput ? e.target.dataset.tagsInput : e.target.parentElement.dataset.tags}"]`).children;
                    for (let i = 0; i < choiceList.length; i++) {
                        isChildFocus = isChildFocus || choiceList[i] == document.activeElement;
                    }
                }

                //If the new focus is not the child remove styling
                if (!isChildFocus) {
                    tagsDisplay.classList.remove('tag-field-focus');
                }
                break;
        }
    }, 200);
}

//Renders chosen items list into the tag field
function renderList(list, tagId) {

    //Delete button for tags
    const deleteButton =
        `<svg onclick="deleteItem(event)" class="delete-button" viewBox="0 0 20 20" fill="none">
            <path d="M10 0C15.53 0 20 4.47 20 10C20 15.53 15.53 20 10 20C4.47 20 0 15.53 0 10C0 4.47 4.47 0 10 0ZM13.59 5L10 8.59L6.41 5L5 6.41L8.59 10L5 13.59L6.41 15L10 11.41L13.59 15L15 13.59L11.41 10L15 6.41L13.59 5Z" fill="#0071BC"/>
        </svg>`

    //Records chosen items list
    const tagDisplay = document.querySelector(`[data-tags-display="${tagId}"]`);

    //Checks if list exists
    if (list && list.length) {
        //Changes all " into &quot; to ensure HTML can read it + renders it into an HTML element
        list.map(value => {
            value = value.split("\"");
            value = value.length > 1 ? value.join("&quot;") : value[0];
            value = value.split("<");
            value = value.length > 1 ? value.join("&lt;") : value[0];
            value = value.split(">");
            value = value.length > 1 ? value.join("&gt;") : value[0];
            return `<span data-tag-of="${tagId}" data-value="${value}" class="chosen-item">${value}${deleteButton}</span>`
        })

            //Adds rendered item to chosen list
            .forEach(element => {
                tagDisplay.innerHTML += element;
            });
    }
}

//Adds choices as selected to hidden slected
function changeSelectValue(list, tagId) {
    //Records chosen items list
    const tagData = document.querySelector(`[data-tags-value="${tagId}"]`);
    tagData.innerHTML = "";

    //Checks if list exists
    if (list && list.length) {

        //Add option to list
        for (let i = 0; i < list.length; i++) {
            tagData.innerHTML += `<option value="${list[i]}"></option>`;
        }

        //Selects all options in list
        for (var i = 0; i < tagData.options.length; i++) {
            tagData.options[i].selected = true;
        }
    }
}

//Functions similarity and editDistance are both for giving a numeric value on the similarity of strings
function similarity(s1, s2) {
    var longer = s1;
    var shorter = s2;
    if (s1.length < s2.length) {
        longer = s2;
        shorter = s1;
    }
    var longerLength = longer.length;
    if (longerLength == 0) {
        return 1.0;
    }
    return (longerLength - editDistance(longer, shorter)) / parseFloat(longerLength);
}

function editDistance(s1, s2) {
    s1 = s1.toLowerCase();
    s2 = s2.toLowerCase();

    var costs = new Array();
    for (var i = 0; i <= s1.length; i++) {
        var lastValue = i;
        for (var j = 0; j <= s2.length; j++) {
            if (i == 0)
                costs[j] = j;
            else {
                if (j > 0) {
                    var newValue = costs[j - 1];
                    if (s1.charAt(i - 1) != s2.charAt(j - 1))
                        newValue = Math.min(Math.min(newValue, lastValue),
                            costs[j]) + 1;
                    costs[j - 1] = lastValue;
                    lastValue = newValue;
                }
            }
        }
        if (i > 0)
            costs[s2.length] = lastValue;
    }
    return costs[s2.length];
}