import { Composition, registerRoot } from "remotion";
import { RAGDemo } from "./compositions/RAGDemo";
import { ArchitectureWalkthrough } from "./compositions/ArchitectureWalkthrough";
import { DeploymentGuide } from "./compositions/DeploymentGuide";

const RemotionRoot = () => {
  return (
    <>
      <Composition
        id="rag-demo"
        component={RAGDemo}
        durationInFrames={180}
        fps={60}
        width={1920}
        height={1080}
        defaultProps={{}}
      />

      <Composition
        id="architecture-walkthrough"
        component={ArchitectureWalkthrough}
        durationInFrames={300}
        fps={60}
        width={1920}
        height={1080}
        defaultProps={{}}
      />

      <Composition
        id="deployment-guide"
        component={DeploymentGuide}
        durationInFrames={240}
        fps={60}
        width={1920}
        height={1080}
        defaultProps={{}}
      />
    </>
  );
};

registerRoot(RemotionRoot);
