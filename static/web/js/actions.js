// $(document).ready(function() {
//     $('#preloader').delay(350).fadeOut('slow');
//  });
function show_loader() {
	$("#global-loader").show();
}

function remove_popup() {
	$("#global-loader").hide();
}

function doAfterAction(action, data, $selector, $after_selector) {
	if (action == "remove_new_employer_popup") {
		var response_data = data["data"];
		$selector.find("button[data-dismiss=modal]").click();
		text = data["text"];
		id = data["id"];
		$after_selector
			.find("#id_employer")
			.html(
				`<option value="${id}" data-select2-id="51">${text}</option>`
			);
		element = `<span class="select2-selection__rendered" id="select2-id_employer-container" role="textbox" aria-readonly="true" title="${text}"><span class="select2-selection__clear" data-select2-id="51" title="Remove all items">×</span>${text}</span>`;
		$after_selector
			.find("#id_employer")
			.siblings("span")
			.find(".select2-selection__rendered")
			.parent()
			.html(element);
	} else if (action == "load_latest_section") {
		$("#modaldemo3").modal("show");
		console.log(
			data,
			$(".form-sections").find(`input[data-term-tab-id=${data.pk}]`)
				.length
		);
		if (
			$(".form-sections").find(`input[data-term-tab-id=${data.pk}]`)
				.length == 0
		) {
			let count = $(".form-sections").find("label").length;

			$(".form-sections")
				.append(`<label style="background-color: #F3F3F3; padding: 5px 10px" class="form-control d-flex align-items-center mb-0 mt-2">
                <input data-term-tab-id=${data.pk} order=${
				count + 1
			} type="checkbox" value=${data.pk} class="" name="checkbox" />
                <span class="mg-l-2">
                    ${data.latest.name}
                </span>
                <a href=${
					data.edit_url
				} class="term_update_modal mg-l-auto reports-edit">
                    <i class="ti-pencil" data-bs-toggle="tooltip" title="" data-bs-original-title="ti-pencil" aria-label="ti-pencil"></i>
                </a>
            </label>`);
		} else {
			$(".form-sections")
				.find(`input[data-term-tab-id=${data.pk}]`)
				.siblings("span")
				.text(`${data.latest.name}`);
		}

		$("#modaldemo3").modal("hide");
	}
}

$(document).ready(function () {
	$(document).on("click", ".check_all_box .list1", function () {
		$parentDiv = $(this).parent("div");
		var unchecked = $parentDiv.find("input.checked").length;
		if (unchecked > 0) {
			$parentDiv.find("input:checkbox").prop("checked", false).change();
			$parentDiv.find("input:checkbox").removeClass("checked");
		} else {
			$parentDiv.find("input:checkbox").prop("checked", true).change();
			$parentDiv.find("input:checkbox").addClass("checked");
		}
	});

	$(".check_items_row input.check").prop("checked", false).change();

	$("a.check_all").click(function (e) {
		e.preventDefault();
		var checked = $(this).hasClass("checked");
		if (checked) {
			$(".check_items_row input.check").prop("checked", false).change();
		} else {
			$(".check_items_row input.check").prop("checked", true).change();
		}
		$(this).toggleClass("checked");
	});

	$(".delete_list_item").hide();

	$("input.check.check_item").change(function () {
		var $this = $(this);
		var checked = $this.prop("checked");
		var data_ids = $(".selected-items-button").attr("data-id");
		var pk = $this.val();
		if (checked) {
			data_ids += pk + ",";
		} else {
			data_ids = data_ids.replace(pk + ",", "");
		}
		$(".selected-items-button").attr("data-id", data_ids);

		if (data_ids != "" && data_ids != undefined && data_ids != null) {
			$(".delete_list_item").show();
		} else {
			$(".delete_list_item").hide();
		}
	});

	$(document).on("click", ".action-button", function (e) {
		e.preventDefault();
		$this = $(this);
		var text = $this.attr("data-text");
		var type = "warning";
		var confirmButtonText = "Yes";
		var confirmButtonColor = "#DD6B55";
		var id = $this.attr("data-id");
		var action = $this.attr("data-action");
		var url = $this.attr("href");
		var title = $this.attr("data-title");
		if (!title) {
			title = "Are you sure?";
		}
		var isReload = $this.hasClass("reload");
		var isRedirect = $this.hasClass("redirect");
		var showAlert = $this.hasClass("with_alert");
		var isRemove = $this.hasClass("remove");
		var noResponsePopup = $this.hasClass("no-response-popup");
		var downloadFile = $this.hasClass("download-file");

		swal(
			{
				title: title,
				text: text,
				type: type,
				showCancelButton: true,
				confirmButtonColor: confirmButtonColor,
				confirmButtonText: confirmButtonText,
				closeOnConfirm: true,
				closeOnCancel: true,
			},
			function (isConfirm) {
				if (isConfirm) {
					show_loader();

					window.setTimeout(function () {
						jQuery.ajax({
							type: action || "GET",
							url: url,
							dataType: "json",
							data: {
								pk: id,
							},
							success: function (data) {
								var message = data["message"];
								var status = data["status"];
								var redirect = data["redirect"];
								var redirect_url = data["redirect_url"];
								var stable = data["stable"];
								var title = data["title"];
								var file_url = data["file_url"];

								remove_popup();

								if (status == "true") {
									if (title) {
										title = title;
									} else {
										title = "Success";
									}
									if (!noResponsePopup) {
										swal(
											{
												title: title,
												text: message,
												type: "success",
											},
											function () {
												if (isRemove) {
													var row_length = $this
														.parents("tbody")
														.find("tr").length;
													$this
														.parents("tr")
														.remove();
													var end = parseInt(
														$(
															".current_end_status"
														).html()
													);
													var total = parseInt(
														$(".total_count").html()
													);
													$(".total_count").html(
														total - 1
													);
													$(
														".current_end_status"
													).html(end - 1);
													if (row_length <= 1) {
														window.location.reload();
													}
												}

												if (stable != "true") {
													if (
														isRedirect &&
														redirect == "true"
													) {
														window.location.href =
															redirect_url;
													}
													if (isReload) {
														window.location.reload();
													}
												}
											}
										);
									}

									if (downloadFile) {
										window.location.href = file_url;
									}
								} else {
									if (title) {
										title = title;
									} else {
										title = "An Error Occurred";
									}

									swal(title, message, "error");

									if (stable != "true") {
										window.setTimeout(function () {}, 2000);
									}
								}
							},
							error: function (data) {
								remove_popup();

								var title = "An error occurred";
								var message =
									"An error occurred. Please try again later.";
								swal(title, message, "error");
							},
						});
					}, 100);
				}
			}
		);
	});

	var $s = $(".form_set_row .check_empty input");
	var e = $s.val();
	if (e == 0 || e == "0") {
		$s.val("");
	}

	$(document).on("submit", "form.ajax", function (e) {
		e.preventDefault();
		var $this = $(this);

		var skip_empty_row = $this.hasClass("skip_empty_row");
		var not_allowed_without_formset = $this.hasClass(
			"not_allowed_without_formset"
		);

		var row_count = $this.find("tr.form_set_row").length;

		if (skip_empty_row) {
			var er = 0;
			$this.find("tr.form_set_row").each(function () {
				$t = $(this);
				var value = $t.find(".check_empty input").val();
				if (!value) {
					if (er == 0) {
						$t.addClass("first");
					}
					er++;
					$t.addClass("delete_row");
				}
			});

			$f = $this.find("tr.form_set_row:first-child");
			if ($f.hasClass("first") && not_allowed_without_formset) {
				$("tr.form_set_row.delete_row")
					.not($f)
					.find("a.icon-trash")
					.click();
			} else {
				$("tr.form_set_row.delete_row").find("a.icon-trash").click();
			}
		}

		var valid = true;
		if (valid) {
			document.onkeydown = function (evt) {
				return false;
			};

			var url = $this.attr("action");
			var method = $this.attr("method");
			var isReset = $this.hasClass("reset");
			var isReload = $this.hasClass("reload");
			var isRedirect = $this.hasClass("redirect");
			var noLoader = $this.hasClass("no-loader");
			var noPopup = $this.hasClass("no-popup");
			var isRunFunctionAfter = $this.hasClass("run-function-after");
			var function_name = $this.attr("data-function");
			var selector_class = $this.attr(
				"data-after-function-selector-parent-class"
			);
			var $after_selector = "";
			if (selector_class) {
				$after_selector = $("." + selector_class);
			}

			var data = $this.serialize();

			if (!noLoader) {
				show_loader();
			}

			data = new FormData(this);
			try {
				data.append(
					e.originalEvent.submitter.name,
					e.originalEvent.submitter.value
				);
			} catch {}

			jQuery.ajax({
				type: method,
				url: url,
				dataType: "json",
				data: data,
				cache: false,
				contentType: false,
				processData: false,
				success: function (data) {
					if (!noLoader) {
						remove_popup();
					}

					var message = data["message"];
					var status = data["status"];
					var title = data["title"];
					var redirect = data["redirect"];
					var redirect_url = data["redirect_url"];
					var new_window = data["new_window"];
					var new_redirect_window = data["new_redirect_window"];
					var new_window_url = data["new_window_url"];
					var popup_redirect = data["popup_redirect"];
					var popup_yes_redirect_url = data["popup_yes_redirect_url"];
					var popup_cancel_redirect_url =
						data["popup_cancel_redirect_url"];
					var popup_redirect_message = data["popup_redirect_message"];
					var stable = data["stable"];
					var pk = data["pk"];

					auto_redirect = $("#auto_redirect").val();
					if (status == "true") {
						if (title) {
							title = title;
						} else {
							title = "Success";
						}

						function doAfter() {
							if (isReset) {
								$this[0].reset();
								$this
									.find(".select2-hidden-accessible")
									.val(null)
									.trigger("change")
									.click();
							}

							console.log(isRunFunctionAfter);

							if (isRunFunctionAfter) {
								doAfterAction(
									function_name,
									data,
									$this,
									$after_selector
								);
							}

							if (stable != "true") {
								if (isRedirect && redirect == "true") {
									if (new_window == "true") {
										window.open(
											redirect_url,
											"_blank" // <- This is what makes it open in a new window.
										);
									} else {
										window.location.href = redirect_url;
									}
								}
								if (isReload) {
									window.location.reload();
								}
								if (isRedirect && popup_redirect == "true") {
									// Show a modal popup - Do you want to create an appointment ?
									window.setTimeout(function () {
										swal(
											{
												title: "Confirm",
												text: popup_redirect_message,
												type: "warning",
												showCancelButton: true,
												confirmButtonColor: "#3085d6",
												cancelButtonColor: "#d33",
												confirmButtonText: "Yes",
												cancelButtonText: "No",
												confirmButtonClass:
													"btn btn-success",
												cancelButtonClass:
													"btn btn-danger",
												buttonsStyling: false,
											},
											function (isConfirm) {
												if (isConfirm) {
													if (pk) {
														fnToCreateAppointment(
															"ENQUIRY_LIST",
															pk
														);
													} else {
														window.location.href =
															popup_yes_redirect_url;
													}
												} else {
													window.location.href =
														popup_cancel_redirect_url;
												}
											}
										);
									}, 200);
								}
							}
						}
						if (new_redirect_window == "true") {
							if (
								new_window_url != "" ||
								new_window_url != null ||
								new_window_url != undefined
							) {
								window.open(new_window_url);
							}
						}

						if (noPopup) {
							doAfter();
						} else {
							swal(
								{
									title: title,
									text: message,
									type: "success",
								},
								function () {
									doAfter();
								}
							);
						}
						document.onkeydown = function (evt) {
							return true;
						};
					} else {
						if (title) {
							title = title;
						} else {
							title = "An Error Occurred";
						}

						swal(title, message, "error");

						if (stable != "true") {
							window.setTimeout(function () {}, 2000);
						}
						document.onkeydown = function (evt) {
							return true;
						};
					}
				},
				error: function (data) {
					remove_popup();

					var title = "An error occurred";
					var message = "An error occurred. Please try again later.";
					document.onkeydown = function (evt) {
						return true;
					};
					swal(title, message, "error");
				},
			});
		}
	});

	$("body").on("focus", "input.datepickerold", function () {
		$(this).datepicker({
			dateFormat: "mm/dd/yy",
			inline: true,
			showOtherMonths: true,
			changeMonth: true,
			changeYear: true,
			dayNamesMin: ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"],
		});
	});
});

function goto_url(url) {
	window.location.href = url;
}

function fnToCreateBill(from_module, object_id = "", params = {}) {
	let URL = "/app/bill/create/?APPOINTMENT_ID=" + object_id;
	goto_url(URL);
}

function fnToCreateAppointment(from_module, object_id = "", params = {}) {
	let URL = "/app/patients/appointments/create-wizard/";
	if (from_module == "ENQUIRY_LIST") {
		URL = "/app/patients/appointments/create/step1/";
	}
	if (from_module == "PATIENT_LIST") {
		URL = "/app/patients/appointments/create/step2/";
	}
	if (from_module) URL += "?FROM=" + from_module;
	if (object_id) {
		if (from_module == "ENQUIRY_LIST") URL += "&ENQUIRY_ID=" + object_id;
		else if (from_module == "PATIENT_LIST")
			URL += "&PATIENT_ID=" + object_id;
	}
	let queryString = Object.keys(params)
		.map((key) => {
			return (
				encodeURIComponent(key) + "=" + encodeURIComponent(params[key])
			);
		})
		.join("&");
	if (queryString) URL += "&" + queryString;
	goto_url(URL);
}

$(".sorter").on("click", function (e) {
	e.preventDefault();
	let base_url = $(this).attr("href");
	let url = window.location.href;
	if (url.includes("sortby=asc")) {
		let goto = base_url.concat("&", "sortby=desc");
		goto_url(goto);
	} else {
		let goto = base_url.concat("&", "sortby=asc");
		goto_url(goto);
	}
});
