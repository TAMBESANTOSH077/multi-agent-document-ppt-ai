import React, {
    useEffect,
    useState,
} from "react";

import "./App.css";

import FileUpload from "./components/FileUpload";
import AgentStatus from "./components/AgentStatus";
import Chat from "./components/Chat";
import ArtifactCard from "./components/ArtifactCard";

import {
    checkBackendHealth,
    sendChatMessage,
} from "./services/api";


export default function App() {

    const [
        backendOnline,
        setBackendOnline,
    ] = useState(false);

    const [
        uploadedFile,
        setUploadedFile,
    ] = useState(null);

    const [
        generating,
        setGenerating,
    ] = useState(false);

    const [
        artifact,
        setArtifact,
    ] = useState(null);

    const [
        error,
        setError,
    ] = useState("");


    /*
     * -------------------------------------------------------
     * Check FastAPI backend
     * -------------------------------------------------------
     */

    useEffect(() => {

        const checkBackend = async () => {

            try {

                await checkBackendHealth();

                setBackendOnline(true);

            } catch (error) {

                console.error(
                    "Backend health check failed:",
                    error
                );

                setBackendOnline(false);
            }
        };


        checkBackend();

        /*
         * Check backend every 10 seconds
         */

        const interval =
            setInterval(
                checkBackend,
                10000
            );


        return () => {
            clearInterval(interval);
        };

    }, []);


    /*
     * -------------------------------------------------------
     * Upload success
     * -------------------------------------------------------
     */

    const handleUploadSuccess =
        (data) => {

            console.log(
                "Uploaded document:",
                data
            );

            setUploadedFile(data);

            setArtifact(null);

            setError("");
        };


    /*
     * -------------------------------------------------------
     * Generate PPT
     * -------------------------------------------------------
     */

    const generatePPT =
        async () => {

            if (!uploadedFile) {

                setError(
                    "Please upload a document first."
                );

                return;
            }


            setGenerating(true);

            setError("");

            setArtifact(null);


            try {

                const fileId =
                    uploadedFile.file_id ||
                    uploadedFile.filename ||
                    null;


                const prompt =
                    `
Create a professional 8-slide PowerPoint
presentation from my uploaded document.

Requirements:

1. Analyze the uploaded document.
2. Extract the important information.
3. Create a professional presentation.
4. Generate exactly 8 slides.
5. Use concise slide content.
6. Include title, overview, key information,
   projects/experience, technical skills,
   important highlights and conclusion where
   applicable.
7. Generate an editable PPTX file.
8. Return the generated PPTX artifact.
                    `.trim();


                const data =
                    await sendChatMessage(
                        prompt,
                        fileId
                    );


                console.log(
                    "PPT generation response:",
                    data
                );


                /*
                 * Backend should return:
                 *
                 * {
                 *     artifact: {
                 *         file_path: "...",
                 *         filename: "..."
                 *     }
                 * }
                 */


                if (!data?.artifact) {

                    throw new Error(
                        "Backend did not return a generated PPTX artifact."
                    );
                }


                setArtifact(
                    data.artifact
                );


            } catch (err) {

                console.error(
                    "PPT generation failed:",
                    err
                );


                setError(
                    err?.message ||
                    "PPT generation failed."
                );


            } finally {

                setGenerating(false);
            }
        };


    /*
     * -------------------------------------------------------
     * Get uploaded filename
     * -------------------------------------------------------
     */

    const uploadedFilename =
        uploadedFile?.filename ||
        uploadedFile?.original_filename ||
        uploadedFile?.name ||
        "Uploaded document";


    /*
     * -------------------------------------------------------
     * Render
     * -------------------------------------------------------
     */

    return (

        <div className="app">


            {/* =================================================
                HEADER
            ================================================= */}

            <header className="header">

                <div>

                    <h1>
                        Multi-Agent Document AI
                    </h1>

                    <p>
                        AI Chatbot for Document &amp;
                        PPT Generation
                    </p>

                </div>


                <div className="tech-badge">

                    FastAPI + React

                </div>

            </header>



            <main className="container">


                {/* =================================================
                    BACKEND STATUS
                ================================================= */}

                <section className="status-card">

                    <div>

                        <h2>
                            Backend Status
                        </h2>

                        <p>
                            FastAPI AI backend
                        </p>

                    </div>


                    <div
                        className={
                            backendOnline
                                ? "online"
                                : "offline"
                        }
                    >

                        <span>
                            ●
                        </span>

                        {backendOnline
                            ? "Online"
                            : "Offline"}

                    </div>

                </section>



                {/* =================================================
                    DOCUMENT UPLOAD
                ================================================= */}

                <FileUpload
                    onUploadSuccess={
                        handleUploadSuccess
                    }
                />



                {/* =================================================
                    DOCUMENT READY
                ================================================= */}

                {uploadedFile && (

                    <section className="success-card">

                        <h3>
                            ✓ Document ready for AI
                        </h3>

                        <p>
                            {uploadedFilename}
                        </p>

                    </section>

                )}



                {/* =================================================
                    MULTI AGENT WORKFLOW
                ================================================= */}

                <AgentStatus />



                {/* =================================================
                    PPT GENERATOR
                ================================================= */}

                {uploadedFile && (

                    <section className="ppt-generator-card">


                        <div className="ppt-icon">
                            📊
                        </div>


                        <div>

                            <h2>
                                Generate PowerPoint
                            </h2>

                            <p>
                                Transform your uploaded
                                document into an editable
                                professional presentation.
                            </p>

                        </div>


                        <button
                            type="button"
                            className="generate-ppt-button"
                            onClick={
                                generatePPT
                            }
                            disabled={
                                generating
                            }
                        >

                            {generating ? (
                                <>
                                    ⏳ Generating...
                                </>
                            ) : (
                                <>
                                    ✨ Generate PPT
                                </>
                            )}

                        </button>

                    </section>

                )}



                {/* =================================================
                    ERROR
                ================================================= */}

                {error && (

                    <div className="error-card">

                        ⚠️ {error}

                    </div>

                )}



                {/* =================================================
                    GENERATED ARTIFACT
                ================================================= */}

                {artifact && (

                    <ArtifactCard
                        artifact={
                            artifact
                        }
                    />

                )}



                {/* =================================================
                    AI CHAT
                ================================================= */}

                <Chat
                    fileId={
                        uploadedFile?.file_id ||
                        uploadedFile?.filename ||
                        null
                    }

                    onResponse={
                        (data) => {

                            console.log(
                                "AI response:",
                                data
                            );


                            /*
                             * If the chatbot itself
                             * generates a document/PPT,
                             * show the artifact.
                             */

                            if (
                                data?.artifact
                            ) {

                                setArtifact(
                                    data.artifact
                                );
                            }

                        }
                    }
                />


            </main>


            {/* =================================================
                FOOTER
            ================================================= */}

            <footer
                style={{
                    textAlign: "center",
                    padding: "25px",
                    color: "#94a3b8",
                    fontSize: "12px",
                }}
            >

                Multi-Agent Document AI
                {" • "}
                Document Intelligence
                {" • "}
                RAG
                {" • "}
                Web Research
                {" • "}
                PPT Generation

            </footer>

        </div>
    );
}