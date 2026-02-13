import React, { useState } from 'react';
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
    Tabs,
    Tab,
    Fade,
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
import { challenges } from './challenges';

function App() {
    const [tabValue, setTabValue] = useState(0);

    const handleTabChange = (event, newValue) => {
        setTabValue(newValue);
    };

    return (
        <Box sx={{ bgcolor: '#f5f5f5', minHeight: '100vh', display: 'flex', flexDirection: 'column' }}>
            {/* Navbar */}
            <AppBar position="sticky" color="default" elevation={2}>
                <Toolbar>
                    <Typography variant="h6" component="div" sx={{ flexGrow: 1, fontWeight: 'bold', color: '#1a237e' }}>
                        IndiaAI Challenge Portal
                    </Typography>
                    <Button color="inherit">Overview</Button>
                    <Button color="inherit">Challenges</Button>
                    <Button variant="contained" color="primary" sx={{ ml: 2 }}>Login</Button>
                </Toolbar>
            </AppBar>

            {/* Hero Section */}
            <Box sx={{
                bgcolor: '#1a237e',
                color: 'white',
                py: 8,
                textAlign: 'center',
                background: 'linear-gradient(135deg, #FF9933 0%, #FFFFFF 50%, #138808 100%)',
                position: 'relative'
            }}>
                <Box sx={{
                    position: 'absolute', top: 0, left: 0, right: 0, bottom: 0,
                    bgcolor: 'rgba(255,255,255,0.8)', zIndex: 1
                }} />
                <Container maxWidth="md" sx={{ position: 'relative', zIndex: 2 }}>
                    <Typography variant="h2" component="h1" gutterBottom sx={{ color: '#1a237e', fontWeight: '800' }}>
                        IndiaAI Solutions Challenge
                    </Typography>
                    <Typography variant="h5" sx={{ mb: 4, color: '#333', fontWeight: 500 }}>
                        Solving Governance, Healthcare, and Financial Compliance for a Digital India
                    </Typography>
                </Container>
            </Box>

            {/* Challenge Categories Tabs */}
            <Container sx={{ mt: -4, mb: 4, position: 'relative', zIndex: 3 }}>
                <Card elevation={3}>
                    <Tabs
                        value={tabValue}
                        onChange={handleTabChange}
                        variant="scrollable"
                        scrollButtons="auto"
                        centered
                        textColor="primary"
                        indicatorColor="primary"
                        sx={{ bgcolor: 'white', borderRadius: 1 }}
                    >
                        {challenges.map((challenge) => (
                            <Tab key={challenge.id} label={challenge.category} />
                        ))}
                    </Tabs>
                </Card>
            </Container>


            {/* Dynamic Challenge Content */}
            <Container sx={{ py: 4, flexGrow: 1 }} maxWidth="lg">
                {challenges.map((category, index) => (
                    <div key={category.id} role="tabpanel" hidden={tabValue !== index}>
                        {tabValue === index && (
                            <Fade in={true} timeout={500}>
                                <Box>
                                    <Box sx={{ mb: 4, textAlign: 'center' }}>
                                        <Typography variant="h4" component="h2" gutterBottom color="primary">
                                            {category.category}
                                        </Typography>
                                        <Typography variant="subtitle1" color="text.secondary">
                                            {category.description}
                                        </Typography>
                                    </Box>
                                    <Grid container spacing={4}>
                                        {category.items.map((prob, idx) => (
                                            <Grid item key={idx} xs={12} sm={6} md={4}>
                                                <Card sx={{ height: '100%', display: 'flex', flexDirection: 'column', transition: '0.3s', '&:hover': { transform: 'translateY(-5px)', boxShadow: 6 } }}>
                                                    <CardMedia
                                                        component="img"
                                                        height="160"
                                                        image={prob.img}
                                                        alt={prob.title}
                                                    />
                                                    <CardContent sx={{ flexGrow: 1 }}>
                                                        <Typography gutterBottom variant="h6" component="h3" sx={{ fontWeight: 'bold' }}>
                                                            {prob.title}
                                                        </Typography>
                                                        <Typography variant="body2" color="text.secondary" paragraph>
                                                            {prob.desc}
                                                        </Typography>
                                                        <Chip label={prob.tag} size="small" color="primary" variant="outlined" />
                                                    </CardContent>
                                                    <CardActions sx={{ p: 2, pt: 0 }}>
                                                        <Button size="small" variant="contained" fullWidth>View Details</Button>
                                                    </CardActions>
                                                </Card>
                                            </Grid>
                                        ))}
                                    </Grid>
                                </Box>
                            </Fade>
                        )}
                    </div>
                ))}
            </Container>

            {/* Timeline */}
            <Box sx={{ bgcolor: 'white', py: 8, mt: 4 }}>
                <Container maxWidth="md">
                    <Typography variant="h4" align="center" gutterBottom sx={{ mb: 4, color: '#1a237e' }}>
                        Roadmap to Innovation
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
                                    Launch
                                </Typography>
                                <Typography variant="body2">Applications Open</Typography>
                            </TimelineContent>
                        </TimelineItem>
                        <TimelineItem>
                            <TimelineOppositeContent color="text.secondary">
                                Mar 15, 2026
                            </TimelineOppositeContent>
                            <TimelineSeparator>
                                <TimelineDot color="warning">
                                    <CodeIcon />
                                </TimelineDot>
                                <TimelineConnector />
                            </TimelineSeparator>
                            <TimelineContent>
                                <Typography variant="h6" component="span">
                                    Prototype Submission
                                </Typography>
                                <Typography variant="body2">Phase 1 Evaluation</Typography>
                            </TimelineContent>
                        </TimelineItem>
                        <TimelineItem>
                            <TimelineOppositeContent color="text.secondary">
                                May 01, 2026
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
                                <Typography variant="body2">Awards & Deployment</Typography>
                            </TimelineContent>
                        </TimelineItem>
                    </Timeline>
                </Container>
            </Box>

            {/* Footer */}
            <Box sx={{ bgcolor: '#263238', color: 'white', p: 6, mt: 'auto' }} component="footer">
                <Grid container spacing={4} justifyContent="center">
                    <Grid item xs={12} sm={4} textAlign="center">
                        <Typography variant="h6" gutterBottom color="#FF9933">
                            IndiaAI Mission
                        </Typography>
                        <Typography variant="body2">
                            Empowering India through Artificial Intelligence. A MeitY initiative.
                        </Typography>
                    </Grid>
                    <Grid item xs={12} sm={4} textAlign="center">
                        <Typography variant="h6" gutterBottom color="#138808">
                            Contact
                        </Typography>
                        <Typography variant="body2">
                            support@indiaai.gov.in
                        </Typography>
                    </Grid>
                </Grid>
                <Typography variant="body2" align="center" sx={{ mt: 4, color: '#90a4ae' }}>
                    {'© '} IndiaAI {new Date().getFullYear()}
                </Typography>
            </Box>
        </Box>
    );
}

export default App;
