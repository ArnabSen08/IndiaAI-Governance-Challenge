// Navigation functionality
document.addEventListener('DOMContentLoaded', function() {
    const navButtons = document.querySelectorAll('.nav-btn');
    const toolSections = document.querySelectorAll('.tool-section');

    navButtons.forEach(button => {
        button.addEventListener('click', () => {
            const toolName = button.dataset.tool;
            
            // Update active nav button
            navButtons.forEach(btn => btn.classList.remove('active'));
            button.classList.add('active');
            
            // Show corresponding tool section
            toolSections.forEach(section => section.classList.remove('active'));
            document.getElementById(`${toolName}-tool`).classList.add('active');
        });
    });

    // Initialize all tools
    initPasswordChecker();
    initCaseConverter();
    initColorContrast();
    initJsonFormatter();
    initQRGenerator();
    initTimezoneConverter();
    initLoremGenerator();
});

// Password Strength Checker
function initPasswordChecker() {
    const passwordInput = document.getElementById('password-input');
    const toggleButton = document.getElementById('toggle-password');
    const strengthBar = document.getElementById('strength-bar');
    const strengthText = document.getElementById('strength-text');
    const passwordTips = document.getElementById('password-tips');

    toggleButton.addEventListener('click', () => {
        const type = passwordInput.type === 'password' ? 'text' : 'password';
        passwordInput.type = type;
        toggleButton.innerHTML = type === 'password' ? '<i class="fas fa-eye"></i>' : '<i class="fas fa-eye-slash"></i>';
    });

    passwordInput.addEventListener('input', () => {
        const password = passwordInput.value;
        const strength = calculatePasswordStrength(password);
        updatePasswordDisplay(strength);
    });

    function calculatePasswordStrength(password) {
        let score = 0;
        const checks = {
            length: password.length >= 8,
            lowercase: /[a-z]/.test(password),
            uppercase: /[A-Z]/.test(password),
            numbers: /\d/.test(password),
            symbols: /[^A-Za-z0-9]/.test(password),
            longLength: password.length >= 12
        };

        // Calculate score
        Object.values(checks).forEach(check => {
            if (check) score++;
        });

        let level = 'Very Weak';
        let color = '#dc3545';
        let percentage = 0;

        if (score >= 5) {
            level = 'Very Strong';
            color = '#28a745';
            percentage = 100;
        } else if (score >= 4) {
            level = 'Strong';
            color = '#20c997';
            percentage = 80;
        } else if (score >= 3) {
            level = 'Medium';
            color = '#ffc107';
            percentage = 60;
        } else if (score >= 2) {
            level = 'Weak';
            color = '#fd7e14';
            percentage = 40;
        } else if (score >= 1) {
            level = 'Very Weak';
            color = '#dc3545';
            percentage = 20;
        }

        return { level, color, percentage, checks, score };
    }

    function updatePasswordDisplay(strength) {
        strengthBar.style.width = `${strength.percentage}%`;
        strengthBar.style.backgroundColor = strength.color;
        strengthText.textContent = `Password Strength: ${strength.level}`;
        strengthText.style.color = strength.color;

        // Update tips
        const tips = [
            { check: strength.checks.length, text: 'At least 8 characters' },
            { check: strength.checks.lowercase, text: 'Contains lowercase letters' },
            { check: strength.checks.uppercase, text: 'Contains uppercase letters' },
            { check: strength.checks.numbers, text: 'Contains numbers' },
            { check: strength.checks.symbols, text: 'Contains special characters' },
            { check: strength.checks.longLength, text: 'At least 12 characters (recommended)' }
        ];

        passwordTips.innerHTML = '<h4>Password Requirements:</h4><ul>' +
            tips.map(tip => 
                `<li><i class="fas ${tip.check ? 'fa-check check' : 'fa-times times'}"></i> ${tip.text}</li>`
            ).join('') + '</ul>';
    }
}

// Case Converter
function initCaseConverter() {
    const caseInput = document.getElementById('case-input');
    const caseOutput = document.getElementById('case-output');
    const caseButtons = document.querySelectorAll('.case-btn');
    const copyButton = document.getElementById('copy-case');

    caseButtons.forEach(button => {
        button.addEventListener('click', () => {
            const caseType = button.dataset.case;
            const inputText = caseInput.value;
            const convertedText = convertCase(inputText, caseType);
            caseOutput.value = convertedText;
        });
    });

    copyButton.addEventListener('click', () => {
        copyToClipboard(caseOutput.value, copyButton);
    });

    function convertCase(text, caseType) {
        if (!text) return '';

        switch (caseType) {
            case 'camel':
                return text.replace(/(?:^\w|[A-Z]|\b\w)/g, (word, index) => {
                    return index === 0 ? word.toLowerCase() : word.toUpperCase();
                }).replace(/\s+/g, '');
            
            case 'pascal':
                return text.replace(/(?:^\w|[A-Z]|\b\w)/g, word => word.toUpperCase()).replace(/\s+/g, '');
            
            case 'snake':
                return text.toLowerCase().replace(/\s+/g, '_').replace(/[^a-z0-9_]/g, '');
            
            case 'kebab':
                return text.toLowerCase().replace(/\s+/g, '-').replace(/[^a-z0-9-]/g, '');
            
            case 'upper':
                return text.toUpperCase();
            
            case 'lower':
                return text.toLowerCase();
            
            case 'title':
                return text.replace(/\w\S*/g, txt => 
                    txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase()
                );
            
            default:
                return text;
        }
    }
}

// Color Contrast Checker
function initColorContrast() {
    const bgColor = document.getElementById('bg-color');
    const bgColorText = document.getElementById('bg-color-text');
    const textColor = document.getElementById('text-color');
    const textColorText = document.getElementById('text-color-text');
    const preview = document.getElementById('contrast-preview');
    const results = document.getElementById('contrast-results');

    // Sync color picker with text input
    bgColor.addEventListener('input', () => {
        bgColorText.value = bgColor.value;
        updateContrast();
    });

    bgColorText.addEventListener('input', () => {
        if (isValidHex(bgColorText.value)) {
            bgColor.value = bgColorText.value;
            updateContrast();
        }
    });

    textColor.addEventListener('input', () => {
        textColorText.value = textColor.value;
        updateContrast();
    });

    textColorText.addEventListener('input', () => {
        if (isValidHex(textColorText.value)) {
            textColor.value = textColorText.value;
            updateContrast();
        }
    });

    function isValidHex(hex) {
        return /^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$/.test(hex);
    }

    function updateContrast() {
        const bg = bgColorText.value;
        const text = textColorText.value;
        
        preview.style.backgroundColor = bg;
        preview.style.color = text;
        
        const ratio = calculateContrastRatio(bg, text);
        displayContrastResults(ratio);
    }

    function hexToRgb(hex) {
        const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
        return result ? {
            r: parseInt(result[1], 16),
            g: parseInt(result[2], 16),
            b: parseInt(result[3], 16)
        } : null;
    }

    function getLuminance(r, g, b) {
        const [rs, gs, bs] = [r, g, b].map(c => {
            c = c / 255;
            return c <= 0.03928 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4);
        });
        return 0.2126 * rs + 0.7152 * gs + 0.0722 * bs;
    }

    function calculateContrastRatio(hex1, hex2) {
        const rgb1 = hexToRgb(hex1);
        const rgb2 = hexToRgb(hex2);
        
        if (!rgb1 || !rgb2) return 1;
        
        const lum1 = getLuminance(rgb1.r, rgb1.g, rgb1.b);
        const lum2 = getLuminance(rgb2.r, rgb2.g, rgb2.b);
        
        const brightest = Math.max(lum1, lum2);
        const darkest = Math.min(lum1, lum2);
        
        return (brightest + 0.05) / (darkest + 0.05);
    }

    function displayContrastResults(ratio) {
        const aaLarge = ratio >= 3;
        const aaNormal = ratio >= 4.5;
        const aaaLarge = ratio >= 4.5;
        const aaaNormal = ratio >= 7;

        results.innerHTML = `
            <div class="contrast-result">
                <div class="contrast-ratio">${ratio.toFixed(2)}:1</div>
                <div>Contrast Ratio</div>
            </div>
            <div class="contrast-result">
                <div>AA Large Text</div>
                <div class="compliance-status ${aaLarge ? 'pass' : 'fail'}">
                    <i class="fas ${aaLarge ? 'fa-check' : 'fa-times'}"></i>
                    ${aaLarge ? 'Pass' : 'Fail'}
                </div>
            </div>
            <div class="contrast-result">
                <div>AA Normal Text</div>
                <div class="compliance-status ${aaNormal ? 'pass' : 'fail'}">
                    <i class="fas ${aaNormal ? 'fa-check' : 'fa-times'}"></i>
                    ${aaNormal ? 'Pass' : 'Fail'}
                </div>
            </div>
            <div class="contrast-result">
                <div>AAA Large Text</div>
                <div class="compliance-status ${aaaLarge ? 'pass' : 'fail'}">
                    <i class="fas ${aaaLarge ? 'fa-check' : 'fa-times'}"></i>
                    ${aaaLarge ? 'Pass' : 'Fail'}
                </div>
            </div>
            <div class="contrast-result">
                <div>AAA Normal Text</div>
                <div class="compliance-status ${aaaNormal ? 'pass' : 'fail'}">
                    <i class="fas ${aaaNormal ? 'fa-check' : 'fa-times'}"></i>
                    ${aaaNormal ? 'Pass' : 'Fail'}
                </div>
            </div>
        `;
    }

    // Initialize with default values
    updateContrast();
}
// JSON Formatter
function initJsonFormatter() {
    const jsonInput = document.getElementById('json-input');
    const jsonOutput = document.getElementById('json-output');
    const formatBtn = document.getElementById('format-json');
    const minifyBtn = document.getElementById('minify-json');
    const validateBtn = document.getElementById('validate-json');
    const copyBtn = document.getElementById('copy-json');
    const status = document.getElementById('json-status');

    formatBtn.addEventListener('click', () => formatJson());
    minifyBtn.addEventListener('click', () => minifyJson());
    validateBtn.addEventListener('click', () => validateJson());
    copyBtn.addEventListener('click', () => copyToClipboard(jsonOutput.value, copyBtn));

    function formatJson() {
        try {
            const parsed = JSON.parse(jsonInput.value);
            jsonOutput.value = JSON.stringify(parsed, null, 2);
            showStatus('JSON formatted successfully!', 'success');
        } catch (error) {
            showStatus(`Invalid JSON: ${error.message}`, 'error');
        }
    }

    function minifyJson() {
        try {
            const parsed = JSON.parse(jsonInput.value);
            jsonOutput.value = JSON.stringify(parsed);
            showStatus('JSON minified successfully!', 'success');
        } catch (error) {
            showStatus(`Invalid JSON: ${error.message}`, 'error');
        }
    }

    function validateJson() {
        try {
            JSON.parse(jsonInput.value);
            showStatus('✅ Valid JSON!', 'success');
        } catch (error) {
            showStatus(`❌ Invalid JSON: ${error.message}`, 'error');
        }
    }

    function showStatus(message, type) {
        status.textContent = message;
        status.className = `json-status ${type}`;
        setTimeout(() => {
            status.textContent = '';
            status.className = 'json-status';
        }, 3000);
    }
}

// QR Code Generator
function initQRGenerator() {
    const qrInput = document.getElementById('qr-input');
    const qrSize = document.getElementById('qr-size');
    const qrCodeDiv = document.getElementById('qr-code');
    const downloadBtn = document.getElementById('download-qr');

    qrInput.addEventListener('input', generateQR);
    qrSize.addEventListener('change', generateQR);

    function generateQR() {
        const text = qrInput.value.trim();
        if (!text) {
            qrCodeDiv.innerHTML = '';
            downloadBtn.style.display = 'none';
            return;
        }

        const size = parseInt(qrSize.value);
        qrCodeDiv.innerHTML = '';

        QRCode.toCanvas(text, {
            width: size,
            height: size,
            margin: 2,
            color: {
                dark: '#000000',
                light: '#FFFFFF'
            }
        }, (error, canvas) => {
            if (error) {
                qrCodeDiv.innerHTML = '<p>Error generating QR code</p>';
                return;
            }
            
            qrCodeDiv.appendChild(canvas);
            downloadBtn.style.display = 'block';
            
            downloadBtn.onclick = () => {
                const link = document.createElement('a');
                link.download = 'qrcode.png';
                link.href = canvas.toDataURL();
                link.click();
            };
        });
    }
}

// Timezone Converter
function initTimezoneConverter() {
    const sourceTime = document.getElementById('source-time');
    const sourceTimezone = document.getElementById('source-timezone');
    const targetTimezone = document.getElementById('target-timezone');
    const results = document.getElementById('timezone-results');

    // Popular timezones
    const timezones = [
        'UTC',
        'America/New_York',
        'America/Chicago',
        'America/Denver',
        'America/Los_Angeles',
        'Europe/London',
        'Europe/Paris',
        'Europe/Berlin',
        'Asia/Tokyo',
        'Asia/Shanghai',
        'Asia/Kolkata',
        'Asia/Dubai',
        'Australia/Sydney',
        'Pacific/Auckland'
    ];

    // Populate timezone selects
    timezones.forEach(tz => {
        const option1 = new Option(tz.replace('_', ' '), tz);
        const option2 = new Option(tz.replace('_', ' '), tz);
        sourceTimezone.appendChild(option1);
        targetTimezone.appendChild(option2);
    });

    // Set default values
    sourceTimezone.value = 'UTC';
    targetTimezone.value = 'America/New_York';
    
    // Set current time
    const now = new Date();
    sourceTime.value = now.toISOString().slice(0, 16);

    sourceTime.addEventListener('change', convertTimezone);
    sourceTimezone.addEventListener('change', convertTimezone);
    targetTimezone.addEventListener('change', convertTimezone);

    function convertTimezone() {
        if (!sourceTime.value) return;

        try {
            const inputDate = new Date(sourceTime.value);
            const sourceZone = sourceTimezone.value;
            const targetZone = targetTimezone.value;

            // Create date in source timezone
            const sourceDate = new Date(inputDate.toLocaleString('en-US', { timeZone: sourceZone }));
            const targetDate = new Date(inputDate.toLocaleString('en-US', { timeZone: targetZone }));

            const options = {
                weekday: 'long',
                year: 'numeric',
                month: 'long',
                day: 'numeric',
                hour: '2-digit',
                minute: '2-digit',
                second: '2-digit',
                timeZoneName: 'short'
            };

            const targetFormatted = inputDate.toLocaleString('en-US', {
                ...options,
                timeZone: targetZone
            });

            results.innerHTML = `
                <div>
                    <strong>From:</strong> ${sourceZone.replace('_', ' ')}<br>
                    ${inputDate.toLocaleString('en-US', { ...options, timeZone: sourceZone })}
                </div>
                <div class="converted-time">
                    ${targetFormatted}
                </div>
                <div>
                    <strong>To:</strong> ${targetZone.replace('_', ' ')}
                </div>
            `;
        } catch (error) {
            results.innerHTML = '<div style="color: #dc3545;">Error converting timezone</div>';
        }
    }

    // Initial conversion
    convertTimezone();
}

// Lorem Ipsum Generator
function initLoremGenerator() {
    const loremType = document.getElementById('lorem-type');
    const loremCount = document.getElementById('lorem-count');
    const generateBtn = document.getElementById('generate-lorem');
    const loremResult = document.getElementById('lorem-result');
    const copyBtn = document.getElementById('copy-lorem');

    const loremWords = [
        'lorem', 'ipsum', 'dolor', 'sit', 'amet', 'consectetur', 'adipiscing', 'elit',
        'sed', 'do', 'eiusmod', 'tempor', 'incididunt', 'ut', 'labore', 'et', 'dolore',
        'magna', 'aliqua', 'enim', 'ad', 'minim', 'veniam', 'quis', 'nostrud',
        'exercitation', 'ullamco', 'laboris', 'nisi', 'aliquip', 'ex', 'ea', 'commodo',
        'consequat', 'duis', 'aute', 'irure', 'in', 'reprehenderit', 'voluptate',
        'velit', 'esse', 'cillum', 'fugiat', 'nulla', 'pariatur', 'excepteur', 'sint',
        'occaecat', 'cupidatat', 'non', 'proident', 'sunt', 'culpa', 'qui', 'officia',
        'deserunt', 'mollit', 'anim', 'id', 'est', 'laborum'
    ];

    generateBtn.addEventListener('click', generateLorem);
    copyBtn.addEventListener('click', () => copyToClipboard(loremResult.value, copyBtn));

    function generateLorem() {
        const type = loremType.value;
        const count = parseInt(loremCount.value);
        let result = '';

        switch (type) {
            case 'words':
                result = generateWords(count);
                break;
            case 'sentences':
                result = generateSentences(count);
                break;
            case 'paragraphs':
                result = generateParagraphs(count);
                break;
        }

        loremResult.value = result;
    }

    function generateWords(count) {
        const words = [];
        for (let i = 0; i < count; i++) {
            words.push(loremWords[Math.floor(Math.random() * loremWords.length)]);
        }
        return words.join(' ');
    }

    function generateSentences(count) {
        const sentences = [];
        for (let i = 0; i < count; i++) {
            const wordCount = Math.floor(Math.random() * 10) + 5; // 5-15 words per sentence
            const words = generateWords(wordCount).split(' ');
            words[0] = words[0].charAt(0).toUpperCase() + words[0].slice(1);
            sentences.push(words.join(' ') + '.');
        }
        return sentences.join(' ');
    }

    function generateParagraphs(count) {
        const paragraphs = [];
        for (let i = 0; i < count; i++) {
            const sentenceCount = Math.floor(Math.random() * 5) + 3; // 3-8 sentences per paragraph
            paragraphs.push(generateSentences(sentenceCount));
        }
        return paragraphs.join('\n\n');
    }

    // Generate initial lorem ipsum
    generateLorem();
}

// Utility function for copying to clipboard
function copyToClipboard(text, button) {
    if (!text) return;
    
    navigator.clipboard.writeText(text).then(() => {
        const originalText = button.innerHTML;
        button.innerHTML = '<i class="fas fa-check"></i> Copied!';
        button.style.background = '#28a745';
        
        setTimeout(() => {
            button.innerHTML = originalText;
            button.style.background = '';
        }, 2000);
    }).catch(() => {
        // Fallback for older browsers
        const textArea = document.createElement('textarea');
        textArea.value = text;
        document.body.appendChild(textArea);
        textArea.select();
        document.execCommand('copy');
        document.body.removeChild(textArea);
        
        const originalText = button.innerHTML;
        button.innerHTML = '<i class="fas fa-check"></i> Copied!';
        button.style.background = '#28a745';
        
        setTimeout(() => {
            button.innerHTML = originalText;
            button.style.background = '';
        }, 2000);
    });
}