# Portfolio Update Guide

## How to Update Your Coursera Portfolio

### Adding New Courses

1. **Edit the HTML file** (`index.html`)
   - Find the courses table section
   - Add new course entries following this format:
   ```html
   <tr>
       <td>Course Name</td>
       <td class="provider">Provider Name</td>
       <td><span class="grade grade-excellent">XX%</span></td>
       <td>Category</td>
   </tr>
   ```

2. **Grade Classes**
   - `grade-excellent`: 90% and above (green)
   - `grade-good`: 80-89% (orange)
   - `grade-average`: Below 80% (red)

3. **Update Statistics**
   - Update the stats cards at the top of the page
   - Modify the numbers in the `.stat-number` divs

### Adding New Specializations

1. **Edit the Specializations Table**
   - Add new rows to the specializations table
   - Use the `specialization-badge` class for status

### Deploying Updates

1. **Commit and Push Changes**
   ```bash
   git add .
   git commit -m "Update portfolio with new courses"
   git push
   ```

2. **Automatic Deployment**
   - GitHub Actions will automatically deploy your changes
   - Your site will be updated at: https://arnabsen08.github.io/coursera-portfolio/

### Repository Structure

```
coursera-portfolio/
├── index.html              # Main portfolio page
├── README.md              # Repository documentation
├── .github/
│   └── workflows/
│       └── deploy.yml     # GitHub Actions deployment
└── update-portfolio.md    # This guide
```

### Tips for Maintenance

- Keep course categories consistent
- Update the average grade calculation when adding courses
- Consider adding new categories as you expand into new learning areas
- The search functionality will automatically work with new courses

### Backup Your Data

- Always keep a backup of your course data
- Consider creating a CSV or JSON file with your course information for easier updates

---

**Need Help?** 
- Check the GitHub repository: https://github.com/ArnabSen08/coursera-portfolio
- Review the GitHub Actions logs if deployment fails
- Ensure all HTML syntax is correct before committing