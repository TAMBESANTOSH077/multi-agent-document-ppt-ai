const API_BASE_URL =
    import.meta.env.VITE_API_BASE_URL ||
    "http://127.0.0.1:8000";


// -----------------------------------------
// Generic request helper
// -----------------------------------------

async function request(
    endpoint,
    options = {}
) {

    const response = await fetch(
        `${API_BASE_URL}${endpoint}`,
        options
    );

    let data = null;

    try {
        data = await response.json();
    } catch {
        data = {};
    }

    if (!response.ok) {

        const message =
            data?.detail ||
            data?.message ||
            "Backend request failed.";

        throw new Error(
            typeof message === "string"
                ? message
                : JSON.stringify(message)
        );
    }

    return data;
}


// -----------------------------------------
// Health
// -----------------------------------------

export async function checkBackendHealth() {

    return request(
        "/health"
    );
}


// -----------------------------------------
// Upload
// -----------------------------------------

export async function uploadFile(
    file
) {

    const formData =
        new FormData();

    formData.append(
        "file",
        file
    );

    return request(
        "/api/upload",
        {
            method: "POST",
            body: formData,
        }
    );
}


// -----------------------------------------
// Chat
// -----------------------------------------

export async function sendChatMessage(
    query,
    fileId = null
) {

    return request(
        "/api/chat",
        {
            method: "POST",

            headers: {
                "Content-Type":
                    "application/json",
            },

            body: JSON.stringify({
                query,
                file_id: fileId,
            }),
        }
    );
}


// -----------------------------------------
// File URL
// -----------------------------------------

export function getFileUrl(
    filePath
) {

    if (!filePath) {
        return "";
    }

    let cleanPath =
        String(filePath)
            .replaceAll("\\", "/");

    // Already a complete URL
    if (
        cleanPath.startsWith(
            "http://"
        ) ||
        cleanPath.startsWith(
            "https://"
        )
    ) {
        return cleanPath;
    }

    // Remove local backend prefixes
    cleanPath =
        cleanPath.replace(
            /^.*?storage[\/\\]/,
            ""
        );

    return (
        `${API_BASE_URL}/storage/` +
        cleanPath
    );
}


export default {
    uploadFile,
    sendChatMessage,
    checkBackendHealth,
    getFileUrl,
};