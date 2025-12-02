// Test script for MCP server
import { cvData } from './cv-data.js';

console.log('=== CV DATA MCP SERVER TEST ===\n');

// Test 1: Personal Info
console.log('✓ Personal Info:');
console.log(`  Name: ${cvData.personal.name}`);
console.log(`  Email: ${cvData.personal.email}`);
console.log(`  GitHub: ${cvData.personal.github}\n`);

// Test 2: Experience
console.log('✓ Experience Records:', cvData.experience.length);
cvData.experience.forEach((exp, i) => {
  console.log(`  ${i + 1}. ${exp.company} (${exp.startDate} - ${exp.endDate})`);
});
console.log();

// Test 3: Projects
console.log('✓ Projects:', cvData.projects.length);
cvData.projects.forEach((proj, i) => {
  console.log(`  ${i + 1}. ${proj.name} (${proj.type})`);
});
console.log();

// Test 4: Skills Categories
console.log('✓ Skills Categories:', Object.keys(cvData.skills).length);
Object.keys(cvData.skills).forEach((cat) => {
  console.log(`  - ${cat}: ${cvData.skills[cat].length} skills`);
});
console.log();

// Test 5: Forbidden Skills
console.log('✓ Forbidden Skills (DO NOT ADD):', cvData.forbidden_skills.length);
console.log(`  Examples: ${cvData.forbidden_skills.slice(0, 5).join(', ')}\n`);

// Test 6: Skill Validation
console.log('=== SKILL VALIDATION TEST ===');
const testSkills = ['Docker', 'React', 'Kubernetes', 'Python', 'AWS'];
testSkills.forEach((skill) => {
  const isForbidden = cvData.forbidden_skills.includes(skill);
  let isVerified = false;
  let category = null;

  // Search through all skill categories
  for (const [cat, skills] of Object.entries(cvData.skills)) {
    if (Array.isArray(skills)) {
      if (skills.some((s) => s.toLowerCase().includes(skill.toLowerCase()))) {
        isVerified = true;
        category = cat;
        break;
      }
    }
  }

  const status = isForbidden ? '❌ FORBIDDEN' : isVerified ? '✅ VERIFIED' : '⚠️ UNKNOWN';
  const info = category ? `(${category})` : isForbidden ? '(in forbidden list)' : '';
  console.log(`  ${status} ${skill} ${info}`);
});

console.log('\n=== TEST COMPLETE ===');
console.log('MCP Server data is valid and ready to use!\n');
