'use client';
import { useState } from 'react';
import { CampaignHeader } from './CampaignHeader';
import { ProgressTracker } from './ProgressTracker';
import { MaterialCanvas } from './MaterialCanvas';
import { CreativeDirectionPreview } from './CreativeDirectionPreview';
import { CopilotInterface } from './CopilotInterface';
import { WorkflowTimeline } from './WorkflowTimeline';
import { UploadSection } from './UploadSection';
import { MoodboardCreator } from './MoodboardCreator';
import { RefinementView } from './RefinementView';
import { PublishingView } from './PublishingView';

export function CampaignStudio() {
  const [currentStep, setCurrentStep] = useState<number>(1);

  const handleBack = () => {
    if (currentStep > 1) {
      setCurrentStep(currentStep - 1);
    }
  };

  return (
    <div className="flex flex-col min-h-screen">
      <CampaignHeader 
        showBack={currentStep > 1} 
        onBack={handleBack} 
      />
      <ProgressTracker activeStep={currentStep} />
      
      <div className="px-12 py-8 flex-1 flex flex-col gap-10">
        {currentStep === 1 && <UploadSection onUpload={() => setCurrentStep(2)} />}
        
        {currentStep === 2 && (
          <>
            <MaterialCanvas />
            <CreativeDirectionPreview onSelectDirection={() => setCurrentStep(3)} />
            <CopilotInterface onSubmit={() => setCurrentStep(3)} />
          </>
        )}

        {currentStep === 3 && (
          <>
            <MoodboardCreator onSelectAsset={() => setCurrentStep(4)} />
            <CopilotInterface onSubmit={() => setCurrentStep(4)} />
          </>
        )}

        {currentStep === 4 && (
          <>
            <RefinementView onApprove={() => setCurrentStep(5)} />
            <CopilotInterface onSubmit={() => setCurrentStep(5)} />
          </>
        )}

        {currentStep === 5 && (
          <PublishingView />
        )}
      </div>
      
      <WorkflowTimeline hasUploaded={currentStep > 1} currentStep={currentStep} />
    </div>
  );
}
