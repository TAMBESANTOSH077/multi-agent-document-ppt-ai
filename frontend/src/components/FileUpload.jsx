import React, {
    useRef,
    useState,
} from "react";

import {
    uploadFile,
} from "../services/api";


const ALLOWED_TYPES = [
    ".pdf",
    ".docx",
    ".ppt",
    ".pptx",
    ".png",
    ".jpg",
    ".jpeg",
    ".webp",
];


export default function FileUpload({
    onUploadSuccess,
}) {

    const fileInputRef =
        useRef(null);

    const [
        selectedFile,
        setSelectedFile,
    ] = useState(null);

    const [
        uploading,
        setUploading,
    ] = useState(false);

    const [
        error,
        setError,
    ] = useState("");

    const [
        success,
        setSuccess,
    ] = useState(false);


    const isValidFile = (
        file
    ) => {

        if (!file) {
            return false;
        }

        const extension =
            "." +
            file.name
                .split(".")
                .pop()
                .toLowerCase();

        return ALLOWED_TYPES.includes(
            extension
        );
    };


    const uploadFileToBackend =
        async (file) => {

            setError("");
            setSuccess(false);

            if (!isValidFile(file)) {

                setError(
                    "Unsupported file type. Please upload PDF, DOCX, PPTX or image."
                );

                return;
            }

            if (
                file.size >
                20 * 1024 * 1024
            ) {

                setError(
                    "File size must be less than 20 MB."
                );

                return;
            }

            setSelectedFile(file);
            setUploading(true);

            try {

                const data =
                    await uploadFile(
                        file
                    );

                console.log(
                    "Upload successful:",
                    data
                );

                setSuccess(true);

                if (
                    onUploadSuccess
                ) {
                    onUploadSuccess(
                        data
                    );
                }

            } catch (error) {

                console.error(
                    "Upload failed:",
                    error
                );

                setError(
                    error.message
                );

            } finally {

                setUploading(false);
            }
        };


    const handleFileChange =
        (event) => {

            const file =
                event.target.files?.[0];

            if (file) {
                uploadFileToBackend(
                    file
                );
            }
        };


    const handleDrop =
        (event) => {

            event.preventDefault();

            const file =
                event.dataTransfer
                    .files?.[0];

            if (file) {
                uploadFileToBackend(
                    file
                );
            }
        };


    const handleDragOver =
        (event) => {

            event.preventDefault();
        };


    return (

        <section className="upload-card">

            <div
                className="upload-zone"
                onClick={() =>
                    fileInputRef.current?.click()
                }
                onDrop={handleDrop}
                onDragOver={
                    handleDragOver
                }
            >

                <div className="upload-icon">
                    📄
                </div>

                <h2>
                    Upload your document
                </h2>

                <p>
                    Drag & drop your file here
                    or click to browse
                </p>

                <button
                    type="button"
                    onClick={(event) => {

                        event.stopPropagation();

                        fileInputRef.current?.click();

                    }}
                    disabled={uploading}
                >

                    {uploading
                        ? "Uploading..."
                        : "Choose File"}

                </button>

                <input
                    ref={fileInputRef}
                    type="file"
                    hidden
                    accept="
                        .pdf,
                        .docx,
                        .ppt,
                        .pptx,
                        .png,
                        .jpg,
                        .jpeg,
                        .webp
                    "
                    onChange={
                        handleFileChange
                    }
                />

            </div>


            {selectedFile && (

                <div className="selected-file">

                    <strong>
                        Selected:
                    </strong>

                    <span>
                        {selectedFile.name}
                    </span>

                </div>

            )}


            {success && (

                <div
                    className="success-card"
                    style={{
                        margin:
                            "0 18px 18px",
                    }}
                >

                    <h3>
                        ✓ File uploaded successfully
                    </h3>

                    <p>
                        Your document is ready
                        for the AI workflow.
                    </p>

                </div>

            )}


            {error && (

                <div
                    className="error-card"
                    style={{
                        margin:
                            "0 18px 18px",
                    }}
                >
                    ⚠️ {error}
                </div>

            )}

        </section>
    );
}