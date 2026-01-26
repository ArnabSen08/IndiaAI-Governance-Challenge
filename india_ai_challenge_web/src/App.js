import React from 'react';
import {
    AppBar,
    Toolbar,
    Typography,
    Button,
    Container,
    Box,
    Grid,
    Card,
    CardContent,
    CardMedia,
    CardActions,
    Chip,
} from '@mui/material';
import {
    Timeline,
    TimelineItem,
    TimelineSeparator,
    TimelineConnector,
    TimelineContent,
    TimelineDot,
    TimelineOppositeContent
} from '@mui/lab';
import RocketLaunchIcon from '@mui/icons-material/RocketLaunch';
import CodeIcon from '@mui/icons-material/Code';
import EmojiEventsIcon from '@mui/icons-material/EmojiEvents';

function App() {
    const problems = [
        {
            title: "AI in Healthcare",
            desc: "Develop AI models for early disease detection and personalized treatment plans using public health datasets.",
            img: "https://source.unsplash.com/random/400x200?medical",
            tag: "Healthcare"
        },
        {
            title: "Agriculture & Supply Chain",
            desc: "Optimize crop yield prediction and supply chain logistics to reduce food wastage using satellite imagery.",
            img: "https://source.unsplash.com/random/400x200?agriculture",
            tag: "Agriculture"
        },
        {
            title: "Financial Fraud Detection",
            desc: "Build robust AI compliance engines to detect banking fraud and validate financial statements against regulations.",
            img: "https://source.unsplash.com/random/400x200?finance",
            tag: "FinTech"
        },
        {
            title: "Smart Cities",
            desc: "Create intelligent traffic management and waste disposal systems for growing urban infrastructure.",
            img: "https://source.unsplash.com/random/400x200?city",
            tag: "Urban"
        }
    ];

    return (
        <Box>
            {/* Navbar */}
            <AppBar position="static" color="default" elevation={1}>
                <Toolbar>
                    <Typography variant="h6" component="div" sx={{ flexGrow: 1, fontWeight: 'bold', color: '#333' }}>
                        IndiaAI Challenge
                    </Typography>
                    <Button color="inherit">About</Button>
                    <Button color="inherit">Problems</Button>
                    <Button color="inherit">Timeline</Button>
                    <Button variant="contained" color="primary">Register Now</Button>
                </Toolbar>
            </AppBar>

            {/* Hero Section */}
            <Box sx={{
                bgcolor: '#1a237e',
                color: 'white',
                py: 10,
                textAlign: 'center',
                background: 'linear-gradient(45deg, #FF9933 30%, #FFFFFF 90%, #138808 100%)'
            }}>
                <Container maxWidth="md">
                    <Typography variant="h2" component="h1" gutterBottom sx={{ color: '#000', fontWeight: '800' }}>
                        IndiaAI Solutions Challenge 2026
                    </Typography>
                    <Typography variant="h5" sx={{ mb: 4, color: '#333' }}>
                        Innovating for a Billion Lives | Jan 26 - Mar 31, 2026
                    </Typography>
                    <Button variant="contained" size="large" sx={{ bgcolor: '#000', color: 'white', px: 5 }}>
                        View Problem Statements
                    </Button>
                </Container>
            </Box>

            {/* Problem Statements */}
            <Container sx={{ py: 8 }} maxWidth="lg">
                <Typography variant="h3" align="center" gutterBottom sx={{ mb: 6 }}>
                    Problem Statements
                </Typography>
                <Grid container spacing={4}>
                    {problems.map((prob, index) => (
                        <Grid item key={index} xs={12} sm={6} md={3}>
                            <Card sx={{ height: '100%', display: 'flex', flexDirection: 'column', transition: '0.3s', '&:hover': { transform: 'scale(1.05)' } }}>
                                <CardMedia
                                    component="img"
                                    height="140"
                                    image={prob.img}
                                    alt={prob.title}
                                />
                                <CardContent sx={{ flexGrow: 1 }}>
                                    <Typography gutterBottom variant="h5" component="h2">
                                        {prob.title}
                                    </Typography>
                                    <Typography>
                                        {prob.desc}
                                    </Typography>
                                    <Chip label={prob.tag} size="small" color="primary" sx={{ mt: 2 }} />
                                </CardContent>
                                <CardActions>
                                    <Button size="small">Details</Button>
                                    <Button size="small">Apply</Button>
                                </CardActions>
                            </Card>
                        </Grid>
                    ))}
                </Grid>
            </Container>

            {/* Timeline */}
            <Box sx={{ bgcolor: '#e3f2fd', py: 8 }}>
                <Container maxWidth="md">
                    <Typography variant="h3" align="center" gutterBottom sx={{ mb: 4 }}>
                        Challenge Timeline
                    </Typography>
                    <Timeline position="alternate">
                        <TimelineItem>
                            <TimelineOppositeContent color="text.secondary">
                                Jan 26, 2026
                            </TimelineOppositeContent>
                            <TimelineSeparator>
                                <TimelineDot color="primary">
                                    <RocketLaunchIcon />
                                </TimelineDot>
                                <TimelineConnector />
                            </TimelineSeparator>
                            <TimelineContent>
                                <Typography variant="h6" component="span">
                                    Applications Open
                                </Typography>
                                <Typography>Register your team and select a problem statement.</Typography>
                            </TimelineContent>
                        </TimelineItem>
                        <TimelineItem>
                            <TimelineOppositeContent color="text.secondary">
                                Feb 20, 2026
                            </TimelineOppositeContent>
                            <TimelineSeparator>
                                <TimelineDot color="secondary">
                                    <CodeIcon />
                                </TimelineDot>
                                <TimelineConnector />
                            </TimelineSeparator>
                            <TimelineContent>
                                <Typography variant="h6" component="span">
                                    Phase 1 Submission
                                </Typography>
                                <Typography>Submit your prototype and technical design.</Typography>
                            </TimelineContent>
                        </TimelineItem>
                        <TimelineItem>
                            <TimelineOppositeContent color="text.secondary">
                                Mar 31, 2026
                            </TimelineOppositeContent>
                            <TimelineSeparator>
                                <TimelineDot color="success">
                                    <EmojiEventsIcon />
                                </TimelineDot>
                            </TimelineSeparator>
                            <TimelineContent>
                                <Typography variant="h6" component="span">
                                    Grand Finale
                                </Typography>
                                <Typography>Final presentation and Winner announcement.</Typography>
                            </TimelineContent>
                        </TimelineItem>
                    </Timeline>
                </Container>
            </Box>

            {/* Footer */}
            <Box sx={{ bgcolor: '#333', color: 'white', p: 6 }} component="footer">
                <Typography variant="h6" align="center" gutterBottom>
                    IndiaAI Mission
                </Typography>
                <Typography variant="subtitle1" align="center" component="p">
                    Ministry of Electronics and Information Technology (MeitY), Government of India
                </Typography>
                <Typography variant="body2" align="center" sx={{ mt: 2, color: '#aaa' }}>
                    Contact: support@indiaai.gov.in | +91-11-2430xxxx
                </Typography>
                <Typography variant="body2" align="center" sx={{ mt: 4, color: '#777' }}>
                    {'Copyright © '} IndiaAI {new Date().getFullYear()}
                </Typography>
            </Box>
        </Box>
    );
}

export default App;
