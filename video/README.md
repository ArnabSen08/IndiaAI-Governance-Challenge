# Ready Tensor Video Project - Remotion Setup Guide

Generate professional demo videos using Remotion.dev

---

## 🎬 About This Project

This is a complete Remotion-based video generation project for creating demo videos of the Ready Tensor RAG system.

**Videos Generated:**
1. **rag-demo.mp4** - 3-minute quick overview
2. **architecture-walkthrough.mp4** - 5-minute technical walkthrough
3. **deployment-guide.mp4** - 4-minute deployment tutorial

---

## 📋 Project Structure

```
video/
├── src/
│   ├── Root.tsx                    # Main composition registry
│   └── compositions/
│       ├── RAGDemo.tsx             # 3-min demo video
│       ├── ArchitectureWalkthrough.tsx  # 5-min architecture video
│       └── DeploymentGuide.tsx     # 4-min deployment video
├── out/                            # Generated MP4 files
├── package.json
└── README.md
```

---

## 🚀 Quick Start

### Prerequisites

```bash
# Required
- Node.js 14+ (or Bun)
- npm or yarn or bun
- FFmpeg (for video rendering)
```

### Step 1: Install Dependencies

```bash
cd video/
npm install
# or
yarn install
# or
bun install
```

### Step 2: View in Remotion Studio

```bash
npm run start
```

Opens http://localhost:3000 where you can:
- Preview videos in real-time
- Edit compositions
- Adjust animations
- Test different frame rates

### Step 3: Render Videos

#### Option A: Render All Videos
```bash
npm run build
```

#### Option B: Render Individual Videos
```bash
# Render RAG demo
npm run render:demo

# Render architecture walkthrough
npm run render:architecture

# Render deployment guide
npm run render:deployment
```

### Step 4: Find Output Files

Videos are saved in `video/out/`:
- `rag-demo.mp4` (3 minutes)
- `architecture-walkthrough.mp4` (5 minutes)
- `deployment-guide.mp4` (4 minutes)

---

## 🎨 Video Compositions

### Video 1: RAGDemo.tsx (180 frames @ 60fps = 3 seconds)

**Content Timeline:**
- **0-2s:** Title animation (fade & scale)
- **1-4s:** Subtitle appears
- **3-6s:** Feature list slides in
- **5-8s:** Performance stats appear
- **7-9s:** Call to action

**Features:**
- Gradient background (purple theme)
- Animated text elements
- Statistics display
- Direct GitHub link

---

### Video 2: ArchitectureWalkthrough.tsx (300 frames @ 60fps = 5 seconds)

**Content Timeline:**
- **0-2.5s:** Title
- **2.5-5s:** Component 1 (User Query)
- **5-7.5s:** Component 2 (Vector Search)
- **7.5-10s:** Component 3 (Context Assembly)
- **10-12.5s:** Component 4 (LLM)
- **12.5-15s:** Component 5 (Output)
- **15-20s:** Performance metrics box

**Features:**
- Dark blue gradient background
- Component-by-component breakdown
- Arrows between components
- Performance stats

---

### Video 3: DeploymentGuide.tsx (240 frames @ 60fps = 4 seconds)

**Content Timeline:**
- **0-2.5s:** Title
- **2.5-5s:** Step 1 (Clone)
- **5-7.5s:** Step 2 (Docker)
- **7.5-10s:** Step 3 (Run)
- **10-15s:** Deployment options box

**Features:**
- Blue-teal gradient background
- Step-by-step instructions
- Command examples
- Deployment option list

---

## 🎯 Customization Guide

### Change Video Duration

Edit `Root.tsx`:
```tsx
// Change durationInFrames for 10 seconds @ 60fps
<Composition
  id="rag-demo"
  durationInFrames={600}  // 600 frames = 10 seconds
  fps={60}
  // ...
/>
```

### Change Video Resolution

Edit `Root.tsx`:
```tsx
// Change to 4K
<Composition
  id="rag-demo"
  width={3840}   // 4K width
  height={2160}  // 4K height
  // ...
/>
```

### Edit Video Content

Edit the composition file (e.g., `RAGDemo.tsx`):

```tsx
// Change title text
<Text style={{ ... }}>Your New Title</Text>

// Change colors
style={{
  background: "linear-gradient(135deg, #newcolor1 0%, #newcolor2 100%)"
}}

// Adjust animations
const opacity = interpolate(frame, [0, 30], [0, 1])
```

### Add Custom Audio

```tsx
import { Audio } from 'remotion';

export const MyVideo = () => {
  return (
    <AbsoluteFill>
      <Audio src="background-music.mp3" />
      {/* Video content */}
    </AbsoluteFill>
  );
};
```

---

## 📊 Rendering Options

### Fast Preview (Lower Quality)
```bash
remotion render src/Root.tsx rag-demo out/preview.mp4 \
  --scale 0.5 \
  --concurrency 1
```

### High Quality (4K)
```bash
remotion render src/Root.tsx rag-demo out/4k.mp4 \
  --width 3840 \
  --height 2160 \
  --concurrency 4
```

### Specific Codec
```bash
remotion render src/Root.tsx rag-demo out/output.mp4 \
  --codec h264 \
  --crf 18  # Quality (18=high, 28=low)
```

---

## 🔧 Advanced Features

### Add Transitions

```tsx
import { Transition } from 'remotion';

<Transition
  durationInFrames={30}
  from={{ opacity: 0 }}
  to={{ opacity: 1 }}
>
  {/* Content */}
</Transition>
```

### Create Animated Counters

```tsx
import { spring, useVideoConfig } from 'remotion';

const animatedValue = spring({
  frame,
  fps: 30,
  config: {
    damping: 200,
  },
});
```

### Add Visual Effects

```tsx
// Blur effect
<div style={{ filter: 'blur(5px)' }}>Content</div>

// Shadow
<div style={{ boxShadow: '0 10px 30px rgba(0,0,0,0.3)' }}>Content</div>

// Rotation
<div style={{ transform: 'rotate(45deg)' }}>Content</div>
```

---

## 📝 Tips & Tricks

### Performance Optimization

1. **Use interpolate() for smooth animations**
   ```tsx
   const value = interpolate(frame, [0, 30], [start, end])
   ```

2. **Keep components focused and small**
   - Prevents re-renders
   - Easier to maintain

3. **Use Sequence for timing control**
   ```tsx
   <Sequence from={50} durationInFrames={60}>
     {/* Renders from frame 50 to 110 */}
   </Sequence>
   ```

### Animation Ideas

- **Fade In/Out:** Interpolate opacity
- **Slide In:** Interpolate transform X/Y
- **Scale:** Interpolate transform scale
- **Rotate:** Interpolate transform rotate
- **Color Shift:** Interpolate colors

### Common Mistakes to Avoid

1. ❌ Don't use hardcoded frame numbers
   - ✅ Use interpolate() instead

2. ❌ Don't create heavy DOM elements
   - ✅ Use CSS transforms for animations

3. ❌ Don't exceed durationInFrames
   - ✅ Keep content within composition duration

---

## 🎥 Exporting Videos

### To YouTube
1. Render MP4
2. Upload to YouTube
3. Add description with GitHub link

### To Social Media (TikTok/Instagram)
```bash
# Render vertical video (9:16)
remotion render src/Root.tsx rag-demo out/vertical.mp4 \
  --width 1080 \
  --height 1920
```

### To GIF (optional)
```bash
remotion render src/Root.tsx rag-demo out/preview.gif
```

---

## 🐛 Troubleshooting

### Issue: "FFmpeg not found"
```bash
# Install FFmpeg
# macOS
brew install ffmpeg

# Windows (with choco)
choco install ffmpeg

# Linux
sudo apt-get install ffmpeg
```

### Issue: "Composition not rendering"
```
1. Check Root.tsx for correct ID
2. Verify component is exported
3. Check frame counts match
```

### Issue: "Slow rendering"
```
- Reduce resolution
- Use fewer concurrent threads
- Simplify animations
- Optimize component structure
```

---

## 📚 Remotion Resources

- **Official Docs:** https://www.remotion.dev/
- **API Reference:** https://www.remotion.dev/docs
- **Examples:** https://github.com/remotion-dev/examples
- **Community Discord:** https://discord.gg/6VzzNDwUwV

---

## 📦 Building for Production

### Create Release Bundle

```bash
# Render all videos in high quality
npm run build

# Verify outputs
ls -lh out/
```

### Upload to Cloud Storage

```bash
# AWS S3
aws s3 cp out/ s3://my-bucket/videos/

# Google Cloud Storage
gsutil -m cp out/* gs://my-bucket/videos/
```

---

## 🎬 Next Steps

1. **Customize videos** with your branding
2. **Add audio** for voiceover/music
3. **Render high-quality versions** for production
4. **Upload to YouTube/social media**
5. **Share in documentation/README**

---

## 📧 Support

For Remotion help:
- Visit https://www.remotion.dev/
- Check Discord community
- Review examples on GitHub

For Ready Tensor help:
- GitHub Issues: https://github.com/ArnabSen08/ready-tensor/issues
- Documentation: /docs folder

---

**Created:** January 2026
**Version:** 1.0.0
**Framework:** Remotion 4.0+
