# HealthRankDash Frontend Testing Instructions

## 🧪 Manual Testing Checklist

### 1. Basic Functionality Test
1. Open http://localhost:3000 in browser
2. Verify page loads with welcome message
3. Check that dropdowns are populated with data
4. Select "California" from State dropdown
5. Verify counties load automatically
6. Select "Premature Death" from Health Indicator dropdown
7. Click "Load Data" button
8. Verify table displays with sample data

### 2. Sorting Functionality Test
1. Load data as above
2. Click on "County" column header - verify ascending sort
3. Click again - verify descending sort
4. Test other column headers (State, Value)
5. Verify sort icons change appropriately
6. Check keyboard accessibility (Tab to header, Enter to sort)

### 3. Confidence Interval Toggle Test
1. Load data with table displayed
2. Check "Show Confidence Intervals" checkbox
3. Verify CI Low and CI High columns appear
4. Uncheck - verify columns disappear
5. Test with keyboard (Tab to checkbox, Space to toggle)

### 4. CSV Export Test
1. Load data with table displayed
2. Click "Export CSV" button
3. Verify file downloads with appropriate filename
4. Open CSV file - verify data matches table
5. Test with different filter combinations

### 5. Filter Interaction Test
1. Select different year options
2. Change state selection - verify counties update
3. Clear filters with "Clear" button
4. Test case-insensitive state selection
5. Verify loading states during filter changes

### 6. Accessibility Testing

#### Keyboard Navigation
1. Tab through entire interface
2. Verify logical tab order
3. Test Skip to Main Content link
4. Use Enter/Space to activate buttons
5. Navigate table with arrow keys
6. Verify focus indicators are visible

#### Screen Reader Testing (if available)
1. Test with VoiceOver (macOS) or NVDA (Windows)
2. Verify all labels are announced
3. Check live region announcements
4. Test table navigation
5. Verify form instructions are read

### 7. Responsive Design Test
1. Test on mobile device (or resize browser to 320px)
2. Verify layout adapts properly
3. Test touch interactions
4. Verify horizontal scroll for table
5. Check button sizes (minimum 44px)

### 8. Error Handling Test
1. Stop backend API (if running)
2. Refresh page
3. Verify graceful fallback to mock data
4. Test network error scenarios
5. Verify error messages are user-friendly

### 9. Progressive Enhancement Test
1. Disable JavaScript in browser
2. Reload page
3. Verify basic structure remains accessible
4. Check noscript warning appears
5. Re-enable JavaScript and verify functionality

### 10. Performance Test
1. Open browser developer tools
2. Go to Network tab
3. Reload page
4. Verify fast loading (under 2 seconds)
5. Check for console errors
6. Test with throttled connection

## 🎯 Success Criteria

All tests should pass with:
- ✅ No console errors
- ✅ Smooth interactions
- ✅ Clear visual feedback
- ✅ Accessible to keyboard users
- ✅ Responsive on all screen sizes
- ✅ Graceful error handling
- ✅ Fast loading performance

## 🔧 Common Issues & Solutions

### Issue: Dropdowns not populating
**Solution**: Check browser console for API errors, verify mock data fallback

### Issue: Table not sorting
**Solution**: Verify data is loaded, check console for JavaScript errors

### Issue: CSV export not working
**Solution**: Check browser popup blocker, verify data is loaded

### Issue: Mobile layout broken
**Solution**: Check CSS media queries, verify responsive classes

### Issue: Accessibility problems
**Solution**: Use browser accessibility tools, verify ARIA attributes

## 📊 Test Results Template

```
Date: ___________
Browser: ___________
Device: ___________

✅ Basic Functionality: PASS/FAIL
✅ Sorting: PASS/FAIL  
✅ CI Toggle: PASS/FAIL
✅ CSV Export: PASS/FAIL
✅ Filters: PASS/FAIL
✅ Accessibility: PASS/FAIL
✅ Responsive: PASS/FAIL
✅ Error Handling: PASS/FAIL
✅ Progressive Enhancement: PASS/FAIL
✅ Performance: PASS/FAIL

Notes: ___________
```

## 🚀 Quick Demo Script

For a 2-minute demo:
1. "This is HealthRankDash, a County Health Rankings explorer"
2. "Select California from the state dropdown"
3. "Choose Premature Death as the health indicator"
4. "Click Load Data to see county comparisons"
5. "Click column headers to sort the data"
6. "Toggle confidence intervals on/off"
7. "Export the data as CSV for further analysis"
8. "Notice the responsive design on mobile"
9. "Everything works with keyboard navigation"
10. "The interface is fully accessible to screen readers"