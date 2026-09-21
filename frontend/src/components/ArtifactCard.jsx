import React from "react";

import {
    getFileUrl,
} from "../services/api";


export default function ArtifactCard({
    artifact,
}) {

    if (!artifact) {
        return null;
    }

    const filePath =
        artifact.file_path ||
        artifact.path ||
        artifact.url;

    const downloadUrl =
        getFileUrl(
            filePath
        );

    const filename =
        artifact.filename ||
        "generated_presentation.pptx";


    return (

        <section className="artifact-card">

            <div className="artifact-icon">
                📊
            </div>

            <div className="artifact-content">

                <h2>
                    Presentation Generated
                </h2>

                <p>
                    Your editable PowerPoint
                    presentation is ready.
                </p>

                <strong>
                    {filename}
                </strong>

                {artifact.slide_count && (
                    <p>
                        {artifact.slide_count}
                        {" "}
                        slides generated
                    </p>
                )}

                {downloadUrl && (

                    <a
                        href={
                            downloadUrl
                        }
                        target="_blank"
                        rel="noreferrer"
                        className="download-button"
                        download
                    >
                        ⬇ Download PPTX
                    </a>

                )}

            </div>

        </section>
    );
}