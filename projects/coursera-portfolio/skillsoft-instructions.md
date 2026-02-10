# How to Add Your Skillsoft Courses

Since I cannot directly read the PDF content, please follow these steps to add your Skillsoft courses to the portfolio:

## 📋 Steps to Update Skillsoft Portfolio

### 1. Open the skillsoft.html file
- The file is already created with a professional template
- It includes your Skillsoft wallet link: https://skillsoft.digitalbadges-eu.skillsoft.com/profile/eu-arnabsen364512/wallet

### 2. Add Your Courses
Replace the sample courses in the table with your actual Skillsoft courses. For each course, add a row like this:

```html
<tr>
    <td>Course Title Here</td>
    <td class="course-category">Category (e.g., Leadership, Technical, Compliance)</td>
    <td><span class="badge badge-certificate">Certificate</span></td> <!-- or badge-digital for Digital Badge -->
    <td><span class="badge badge-completed">Completed</span></td>
    <td>YYYY-MM-DD</td> <!-- Completion date -->
</tr>
```

### 3. Badge Types Available
- `badge-certificate` - For certificates (orange)
- `badge-digital` - For digital badges (blue)
- `badge-completed` - For completion status (green)

### 4. Course Categories
Common categories you might use:
- Leadership
- Management
- Technical
- Security/Cybersecurity
- Compliance
- Innovation
- Communication
- Project Management
- Data Analysis
- Software Development

### 5. Example Course Entry
```html
<tr>
    <td>Advanced Project Management</td>
    <td class="course-category">Management</td>
    <td><span class="badge badge-certificate">Certificate</span></td>
    <td><span class="badge badge-completed">Completed</span></td>
    <td>2024-01-15</td>
</tr>
```

## 📊 Automatic Features
The page automatically:
- Counts total courses
- Counts digital badges vs certificates
- Estimates learning hours (2 hours per course)
- Provides search functionality
- Links to both Coursera and Skillsoft portfolios

## 🔄 After Adding Courses
1. Save the skillsoft.html file
2. Commit and push to GitHub:
   ```bash
   git add skillsoft.html
   git commit -m "Add Skillsoft courses from Hitachi Energy training"
   git push
   ```
3. The page will be automatically deployed to: https://arnabsen08.github.io/coursera-portfolio/skillsoft.html

## 📝 From Your PDF
Look for these details in your Skillsoft Course List PDF:
- Course names/titles
- Completion dates
- Badge types (certificate vs digital badge)
- Course categories or subjects
- Any additional details like learning hours

Copy this information into the HTML table format above, replacing the sample courses.

## 🎯 Navigation
The portfolio now has navigation between:
- Main Coursera portfolio (index.html)
- Skillsoft portfolio (skillsoft.html)

Both pages are professionally styled and mobile-responsive!