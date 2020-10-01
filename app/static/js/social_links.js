$(window).on("load", () => {
	$(".social-del").click(deleteSocialInput);

	$(".social-add").click(e => {
		e.preventDefault();
		
		const newSelect = $("<select></select>")
			.prop("name", "social-type")
			.addClass("form-group-label")
			.addClass("btn-grey")
			.addClass("select")
			.change(updatePlaceholder);

		for (let type in SOCIAL_TYPES) {
			const opt = $("<option></option>")
				.val(type)
				.text(type);
			newSelect.append(opt);
		}

		const newInput = $("<input>")
			.addClass("form-group-input")
			.prop("type", "text")
			.prop("name", "social-content")
			.prop("placeholder", SOCIAL_TYPES[Object.keys(SOCIAL_TYPES)[0]])
			.prop("required", true);

		const newBtn = $("<button></button>")
			.addClass("form-group-btn")
			.addClass("social-del")
			.text("x")
			.click(deleteSocialInput);

		const newField = $("<div></div>")
			.addClass("form-group")
			.append(newSelect, newInput, newBtn);

		$(".social-inputs").append(newField);
	});

	// add onchange to current select fields
	$(".social-inputs select").change(updatePlaceholder);

	// enable after the click handler has been added
	$(".social-add, .social-del").prop("disabled",false);
});

function updatePlaceholder() {
	$(this).parent().find("input[type='text']").first().prop("placeholder", SOCIAL_TYPES[$(this).val()]);
}

function deleteSocialInput(e) {
	e.preventDefault();
	$(this).parent().remove();
}
