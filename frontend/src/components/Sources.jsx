import React from "react";

function Sources({ sources = [] }) {
    if (!sources.length) {
        return null;
    }

    return (
        <div style={styles.container}>
            <h2>Sources & Traceability</h2>

            {sources.map(
                (source, index) => (
                    <div
                        key={index}
                        style={styles.source}
                    >
                        <strong>
                            {source.title ||
                                `Source ${index + 1}`}
                        </strong>

                        {source.url && (
                            <a
                                href={source.url}
                                target="_blank"
                                rel="noreferrer"
                                style={styles.link}
                            >
                                {source.url}
                            </a>
                        )}

                        {source.score !==
                            undefined && (
                            <small>
                                Relevance:{" "}
                                {Number(
                                    source.score
                                ).toFixed(3)}
                            </small>
                        )}
                    </div>
                )
            )}
        </div>
    );
}

const styles = {
    container: {
        background: "#ffffff",
        padding: "22px",
        borderRadius: "18px",
        border: "1px solid #e2e8f0",
        marginBottom: "20px",
    },

    source: {
        padding: "14px",
        borderRadius: "10px",
        background: "#f8fafc",
        marginBottom: "10px",
        display: "flex",
        flexDirection: "column",
        gap: "5px",
    },

    link: {
        color: "#2563eb",
        wordBreak: "break-all",
    },
};

export default Sources;