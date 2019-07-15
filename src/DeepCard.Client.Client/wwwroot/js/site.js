"use strict";

function getFileInputLength(element) {
    return element.files.length;
}

function getFileInputItemName(element, index) {
    return element.files[index].name;
}

function getFileInputItemSize(element, index) {
    return element.files[index].size;
}

function getFileInputClear(element) {
    return element.value = "";
}

function getFileInputDataBase64(element, index) {
    const temporaryFileReader = new FileReader();
    return new Promise((resolve, reject) => {
        temporaryFileReader.onerror = () => {
            temporaryFileReader.abort();
            reject(new DOMException("Problem parsing input file."));
        };
        temporaryFileReader.addEventListener("load", function () {
            resolve(temporaryFileReader.result.split(',')[1]);
        }, false);
        temporaryFileReader.readAsDataURL(element.files[index]);
    });
}