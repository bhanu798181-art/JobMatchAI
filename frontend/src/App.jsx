import { useEffect, useState } from "react";
import "./App.css";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

function App() {
const [email, setEmail] = useState("");
const [password, setPassword] = useState("");

const [user, setUser] = useState(null);
const [checkingSession, setCheckingSession] = useState(true);
useEffect(() => {
  async function checkSession() {
    try {
      const response = await fetch(
        `${API_URL}/auth/me`,
        {
          method: "GET",
          credentials: "include",
          headers: {
            Accept: "application/json",
          },
        }
      );

      if (!response.ok) {
        setUser(null);
        return;
      }

      const data = await response.json();

if (data.user) {
  setUser(data.user);

  // Reload saved data after page refresh
  if (data.user.role === "student") {
    await loadProfile();
    await loadEducation();
    await loadJobs();
    await loadApplications();
    await loadSkills();
  }

if (data.user.role === "company") {
  await loadCompanyJobs();
  await loadCompanyApplications();
}

} else {
  setUser(null);
}

    } catch (error) {
      console.error(
        "Session check failed:",
        error
      );

      setUser(null);

    } finally {
      setCheckingSession(false);
    }
  }

  checkSession();
}, []);

// Registration
const [showRegister, setShowRegister] = useState(false);
const [registerEmail, setRegisterEmail] = useState("");
const [registerPassword, setRegisterPassword] = useState("");
const [registerRole, setRegisterRole] = useState("student");
const [registering, setRegistering] = useState(false);
const [registerError, setRegisterError] = useState("");
const [registerMessage, setRegisterMessage] = useState("");

// Student matching jobs
const [jobs, setJobs] = useState([]);

// Company dashboard jobs
const [jobSearch, setJobSearch] = useState("");
const [jobLocationFilter, setJobLocationFilter] = useState("");
const [jobWorkModeFilter, setJobWorkModeFilter] = useState("");
const [jobEmploymentFilter, setJobEmploymentFilter] = useState("");
const [jobSourceFilter, setJobSourceFilter] = useState("");
const [jobMinSalaryFilter, setJobMinSalaryFilter] = useState("");
const [companyJobs, setCompanyJobs] = useState([]);
const [loadingCompanyJobs, setLoadingCompanyJobs] = useState(false);
const [companyJobsError, setCompanyJobsError] = useState("");
  const [studentProfile, setStudentProfile] = useState(null);
const [loadingProfile, setLoadingProfile] = useState(false);
const [editingProfile, setEditingProfile] = useState(false);
const [savingProfile, setSavingProfile] = useState(false);
const [profileError, setProfileError] = useState("");

const [profileForm, setProfileForm] = useState({
  full_name: "",
  phone: "",
  city: "",
  state: "",
  country: "",

  qualification: "",
  degree_name: "",
  branch: "",
  college: "",
  graduation_year: "",
  cgpa: "",
  percentage: "",
});
const [studentEducation, setStudentEducation] = useState([]);
const [loadingEducation, setLoadingEducation] = useState(false);
const [educationError, setEducationError] = useState("");
  const [applications, setApplications] = useState([]);
  // Company applications
const [companyApplications, setCompanyApplications] = useState([]);
const [loadingCompanyApplications, setLoadingCompanyApplications] =
  useState(false);
const [companyApplicationsError, setCompanyApplicationsError] =
  useState("");

  // Student skills
  const [allSkills, setAllSkills] = useState([]);
  const [studentSkills, setStudentSkills] = useState([]);
  const [loadingSkills, setLoadingSkills] = useState(false);
  const [skillsError, setSkillsError] = useState("");
  const [selectedSkillId, setSelectedSkillId] = useState("");
  const [skillProficiency, setSkillProficiency] = useState("");
  const [savingSkill, setSavingSkill] = useState(false);

  const [loadingJobs, setLoadingJobs] = useState(false);
  const [loadingApplications, setLoadingApplications] = useState(false);
  const [loggingIn, setLoggingIn] = useState(false);

  const [loginError, setLoginError] = useState("");
  const [jobsError, setJobsError] = useState("");
  const [applicationsError, setApplicationsError] = useState("");

  const [selectedJob, setSelectedJob] = useState(null);
  const [jobDetailsLoading, setJobDetailsLoading] = useState(false);

  const [applying, setApplying] = useState(false);
  const [applicationMessage, setApplicationMessage] = useState("");

  // Application management
  const [selectedApplication, setSelectedApplication] = useState(null);
  const [applicationActionLoading, setApplicationActionLoading] =
    useState(false);

  const [editingApplication, setEditingApplication] = useState(null);
  const [editStatus, setEditStatus] = useState("");
  const [editNotes, setEditNotes] = useState("");

  // ==================================================
  // LOAD MATCHING JOBS
  // ==================================================

  async function loadJobs() {
  setLoadingJobs(true);
  setJobsError("");

  try {
    const response = await fetch(`${API_URL}/matching/jobs`, {
      method: "GET",
      credentials: "include",
      headers: {
        Accept: "application/json",
      },
    });

    if (!response.ok) {
      throw new Error(`Request failed: ${response.status}`);
    }

    const data = await response.json();

    // Always show the strongest matches first.
    const sortedJobs = [...data].sort(
      (a, b) =>
        Number(b.match_score || 0) -
        Number(a.match_score || 0)
    );

    setJobs(sortedJobs);

  } catch (error) {
    console.error("Matching jobs error:", error);

    setJobsError(
      "Unable to load matching jobs. Please make sure you are logged in."
    );
  } finally {
    setLoadingJobs(false);
  }
}
// ==================================================
// LOAD COMPANY APPLICATIONS
// ==================================================

async function loadCompanyApplications() {
  setLoadingCompanyApplications(true);
  setCompanyApplicationsError("");

  try {
    const response = await fetch(
      `${API_URL}/applications/company`,
      {
        method: "GET",
        credentials: "include",
        headers: {
          Accept: "application/json",
        },
      }
    );

    const data = await response.json();

    if (!response.ok) {
      throw new Error(
        data.detail || "Unable to load applications"
      );
    }

    setCompanyApplications(
      Array.isArray(data) ? data : []
    );

  } catch (error) {
    console.error(
      "Company applications error:",
      error
    );

    setCompanyApplicationsError(
      error.message ||
        "Unable to load company applications."
    );

    setCompanyApplications([]);
  } finally {
    setLoadingCompanyApplications(false);
  }
}

// ==================================================
// UPDATE COMPANY APPLICATION STATUS
// ==================================================

async function handleCompanyApplicationStatus(
  applicationId,
  newStatus
) {
  try {
    const response = await fetch(
      `${API_URL}/applications/company/${applicationId}/status`,
      {
        method: "PUT",
        credentials: "include",
        headers: {
          Accept: "application/json",
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          application_status: newStatus,
        }),
      }
    );

    const data = await response.json();

    if (!response.ok) {
      throw new Error(
        data.detail ||
          "Unable to update application status"
      );
    }

    // Update the application immediately on screen
    setCompanyApplications((currentApplications) =>
      currentApplications.map((application) =>
        application.id === applicationId
          ? {
              ...application,
              application_status:
                data.application_status,
            }
          : application
      )
    );

  } catch (error) {
    console.error(
      "Company application status error:",
      error
    );

    alert(
      error.message ||
        "Unable to update application status."
    );
  }
}
// ==================================================
// LOAD COMPANY JOBS
// ==================================================

async function loadCompanyJobs() {
  setLoadingCompanyJobs(true);
  setCompanyJobsError("");

  try {
    const response = await fetch(
      `${API_URL}/jobs/my`,
      {
        method: "GET",
        credentials: "include",
        headers: {
          Accept: "application/json",
        },
      }
    );

    const data = await response.json();

    if (!response.ok) {
      throw new Error(
        typeof data.detail === "string"
          ? data.detail
          : `Request failed: ${response.status}`
      );
    }

    setCompanyJobs(data);

  } catch (error) {
    console.error("Company jobs error:", error);

    setCompanyJobsError(
      error.message || "Unable to load company jobs."
    );

  } finally {
    setLoadingCompanyJobs(false);
  }
}
  // ==================================================
  // LOAD APPLICATIONS
  // ==================================================

  async function loadApplications() {
    setLoadingApplications(true);
    setApplicationsError("");

    try {
      const response = await fetch(`${API_URL}/applications`, {
        method: "GET",
        credentials: "include",
        headers: {
          Accept: "application/json",
        },
      });

      if (!response.ok) {
        throw new Error(`Request failed: ${response.status}`);
      }

      const data = await response.json();

      setApplications(data);
    } catch (error) {
      console.error("Applications error:", error);

      setApplicationsError(
        "Unable to load your applications."
      );
    } finally {
      setLoadingApplications(false);
    }
  }

  // ==================================================
// LOAD PROFILE
// ==================================================

async function loadProfile() {
  setLoadingProfile(true);
  setProfileError("");

  try {
    const response = await fetch(
      `${API_URL}/profile`,
      {
        method: "GET",
        credentials: "include",
        headers: {
          Accept: "application/json",
        },
      }
    );

    const data = await response.json();

    if (!response.ok) {
      throw new Error(
        typeof data.detail === "string"
          ? data.detail
          : "Unable to load profile."
      );
    }

    setStudentProfile(data);

    setProfileForm({
      full_name: data.full_name || "",
      phone: data.phone || "",
      city: data.city || "",
      state: data.state || "",
      country: data.country || "",
    });

  } catch (error) {
    console.error(
      "Profile loading error:",
      error
    );

    setProfileError(
      error.message ||
        "Unable to load your profile."
    );

  } finally {
    setLoadingProfile(false);
  }
}
// ==================================================
// LOAD EDUCATION
// ==================================================

async function loadEducation() {
  setLoadingEducation(true);
  setEducationError("");

  try {
    const response = await fetch(
      `${API_URL}/profile/education`,
      {
        method: "GET",
        credentials: "include",
        headers: {
          Accept: "application/json",
        },
      }
    );

    const data = await response.json();

    if (!response.ok) {
      throw new Error(
        typeof data.detail === "string"
          ? data.detail
          : "Unable to load education."
      );
    }

    setStudentEducation(
      Array.isArray(data) ? data : []
    );

  } catch (error) {
    console.error(
      "Education loading error:",
      error
    );

    setEducationError(
      error.message ||
        "Unable to load education."
    );

  } finally {
    setLoadingEducation(false);
  }
}

// ==================================================
// UPDATE PROFILE
// ==================================================

async function handleUpdateProfile(event) {
  event.preventDefault();

  setSavingProfile(true);
  setProfileError("");

  try {
    const response = await fetch(
      `${API_URL}/profile`,
      {
        method: "PUT",
        credentials: "include",
        headers: {
          Accept: "application/json",
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          full_name: profileForm.full_name,
          phone: profileForm.phone || null,
          city: profileForm.city || null,
          state: profileForm.state || null,
          country: profileForm.country || null,
        }),
      }
    );

    const data = await response.json();

    if (!response.ok) {
      let message = "Unable to update profile.";

      if (typeof data.detail === "string") {
        message = data.detail;
      } else if (Array.isArray(data.detail)) {
        message = data.detail
          .map(
            (item) =>
              item.msg ||
              "Invalid profile information"
          )
          .join(", ");
      }

      throw new Error(message);
    }

    setStudentProfile(data);

    setProfileForm({
      full_name: data.full_name || "",
      phone: data.phone || "",
      city: data.city || "",
      state: data.state || "",
      country: data.country || "",
    });

    setEditingProfile(false);

    await loadJobs();

    alert("Profile updated successfully!");

  } catch (error) {
    console.error(
      "Profile update error:",
      error
    );

    setProfileError(
      error.message ||
        "Unable to update your profile."
    );

  } finally {
    setSavingProfile(false);
  }
}
async function handleUpdateProfile(event) {
  event.preventDefault();

  setSavingProfile(true);
  setProfileError("");

  try {
    // ----------------------------------------------
    // UPDATE PERSONAL PROFILE
    // ----------------------------------------------

    const response = await fetch(
      `${API_URL}/profile`,
      {
        method: "PUT",
        credentials: "include",
        headers: {
          Accept: "application/json",
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          full_name: profileForm.full_name,
          phone: profileForm.phone || null,
          city: profileForm.city || null,
          state: profileForm.state || null,
          country: profileForm.country || null,
        }),
      }
    );

    const data = await response.json();

    if (!response.ok) {
      let message = "Unable to update profile.";

      if (typeof data.detail === "string") {
        message = data.detail;
      } else if (Array.isArray(data.detail)) {
        message = data.detail
          .map(
            (item) =>
              item.msg ||
              "Invalid profile information"
          )
          .join(", ");
      }

      throw new Error(message);
    }

// ----------------------------------------------
// CREATE / UPDATE EDUCATION
// ----------------------------------------------

if (!profileForm.qualification?.trim()) {
  setEditingProfile(false);

  await loadJobs();

  alert("Profile updated successfully!");

  return;
}

const educationPayload = {
  qualification:
    profileForm.qualification || null,

  degree_name:
    profileForm.degree_name || null,

  branch:
    profileForm.branch || null,

  college:
    profileForm.college || null,

  graduation_year:
    profileForm.graduation_year
      ? Number(profileForm.graduation_year)
      : null,

  cgpa:
    profileForm.cgpa !== ""
      ? Number(profileForm.cgpa)
      : null,

  percentage:
    profileForm.percentage !== ""
      ? Number(profileForm.percentage)
      : null,
};

const educationExists =
  studentEducation.length > 0;

const educationUrl = educationExists
  ? `${API_URL}/profile/education/${studentEducation[0].id}`
  : `${API_URL}/profile/education`;

const educationMethod = educationExists
  ? "PUT"
  : "POST";

const educationResponse = await fetch(
  educationUrl,
  {
    method: educationMethod,
    credentials: "include",
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(
      educationPayload
    ),
  }
);

const educationData =
  await educationResponse.json();

if (!educationResponse.ok) {

  let message =
    educationExists
      ? "Unable to update education."
      : "Unable to save education.";

  if (
    typeof educationData.detail ===
    "string"
  ) {
    message = educationData.detail;
  } else if (
    Array.isArray(educationData.detail)
  ) {
    message = educationData.detail
      .map(
        (item) =>
          item.msg ||
          "Invalid education information"
      )
      .join(", ");
  }

  throw new Error(message);
}

// Update education displayed on the page
setStudentEducation([
  educationData,
]);


    // ----------------------------------------------
    // UPDATE PROFILE STATE
    // ----------------------------------------------

    setStudentProfile(data);

    setProfileForm({
      full_name: data.full_name || "",
      phone: data.phone || "",
      city: data.city || "",
      state: data.state || "",
      country: data.country || "",

      qualification:
        studentEducation[0]?.qualification || "",

      degree_name:
        studentEducation[0]?.degree_name || "",

      branch:
        studentEducation[0]?.branch || "",

      college:
        studentEducation[0]?.college || "",

      graduation_year:
        studentEducation[0]?.graduation_year || "",

      cgpa:
        studentEducation[0]?.cgpa ?? "",

      percentage:
        studentEducation[0]?.percentage ?? "",
    });

    setEditingProfile(false);

    // Refresh job matches because education
    // affects the matching score.
    await loadJobs();

    alert(
      "Profile and education updated successfully!"
    );

  } catch (error) {
    console.error(
      "Profile update error:",
      error
    );

    setProfileError(
      error.message ||
        "Unable to update your profile."
    );

  } finally {
    setSavingProfile(false);
  }
}

// ==================================================
// LOAD SKILLS
// ==================================================

  async function loadSkills() {
    setLoadingSkills(true);
    setSkillsError("");

    try {
      const [allResponse, studentResponse] = await Promise.all([
        fetch(`${API_URL}/profile/skills/all`, {
          method: "GET",
          credentials: "include",
          headers: { Accept: "application/json" },
        }),
        fetch(`${API_URL}/profile/skills`, {
          method: "GET",
          credentials: "include",
          headers: { Accept: "application/json" },
        }),
      ]);

      const allData = await allResponse.json();
      const studentData = await studentResponse.json();

      if (!allResponse.ok) {
        throw new Error(allData.detail || "Unable to load available skills");
      }

      if (!studentResponse.ok) {
        throw new Error(studentData.detail || "Unable to load your skills");
      }

      setAllSkills(allData);
      setStudentSkills(studentData);
    } catch (error) {
      console.error("Skills error:", error);
      setSkillsError(error.message || "Unable to load skills.");
    } finally {
      setLoadingSkills(false);
    }
  }

  // ==================================================
  // ADD STUDENT SKILL
  // ==================================================

  async function handleAddSkill(event) {
    event.preventDefault();

    if (!selectedSkillId) {
      return;
    }

    if (!skillProficiency) {
      setSkillsError("Please select a proficiency level.");
      return;
    }

    setSavingSkill(true);
    setSkillsError("");

    try {
      const response = await fetch(`${API_URL}/profile/skills`, {
        method: "POST",
        credentials: "include",
        headers: {
          Accept: "application/json",
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          skill_id: Number(selectedSkillId),
          proficiency: skillProficiency,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Unable to add skill");
      }

      await loadSkills();

      setSelectedSkillId("");
      setSkillProficiency("");

      // Skill changes should immediately affect recommendations.
      await loadJobs();
    } catch (error) {
      console.error("Add skill error:", error);
      setSkillsError(error.message || "Unable to add skill.");
    } finally {
      setSavingSkill(false);
    }
  }

  // ==================================================
  // REMOVE STUDENT SKILL
  // ==================================================

  async function handleRemoveSkill(skillId) {
    const confirmed = window.confirm(
      "Remove this skill from your profile?"
    );

    if (!confirmed) return;

    setSavingSkill(true);
    setSkillsError("");

    try {
      const response = await fetch(
        `${API_URL}/profile/skills/${skillId}`,
        {
          method: "DELETE",
          credentials: "include",
          headers: { Accept: "application/json" },
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Unable to remove skill");
      }

      await loadSkills();

      // Skill changes should immediately affect recommendations.
      await loadJobs();
    } catch (error) {
      console.error("Remove skill error:", error);
      setSkillsError(error.message || "Unable to remove skill.");
    } finally {
      setSavingSkill(false);
    }
  }

 // ==================================================
// LOGIN
// ==================================================

async function handleLogin(event) {
  event.preventDefault();

  setLoggingIn(true);
  setLoginError("");

  try {
    const response = await fetch(`${API_URL}/auth/login`, {
      method: "POST",
      credentials: "include",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        email: email,
        password: password,
      }),
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.detail || "Login failed");
    }

    // Save the logged-in user
    setUser(data.user);

    // ==================================================
    // STUDENT LOGIN
    // ==================================================

    if (data.user.role === "student") {
      await loadProfile();
      await loadEducation();
      await loadJobs();
      await loadApplications();
      await loadSkills();
    }

    // ==================================================
    // COMPANY LOGIN
    // ==================================================

if (data.user.role === "company") {
  await loadCompanyJobs();
  await loadCompanyApplications();
}

  } catch (error) {
    console.error("Login error:", error);
    setLoginError(error.message);

  } finally {
    setLoggingIn(false);
  }
}
// ==================================================
// REGISTRATION
// ==================================================

async function handleRegister(event) {
  event.preventDefault();

  setRegistering(true);
  setRegisterError("");
  setRegisterMessage("");

  try {
    const response = await fetch(`${API_URL}/auth/register`, {
      method: "POST",
      credentials: "include",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        email: registerEmail,
        password: registerPassword,
        role: registerRole,
      }),
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(
        data.detail || "Registration failed"
      );
    }

    setRegisterMessage(
      data.message || "Registration successful. You can now login."
    );

    setEmail(registerEmail);
    setPassword("");

    setRegisterEmail("");
    setRegisterPassword("");

  } catch (error) {
    console.error("Registration error:", error);
    setRegisterError(error.message);
  } finally {
    setRegistering(false);
  }
}
  // ==================================================
  // LOGOUT
  // ==================================================

async function handleLogout() {
  try {
    await fetch(
      `${API_URL}/auth/logout`,
      {
        method: "POST",
        credentials: "include",
        headers: {
          Accept: "application/json",
        },
      }
    );
  } catch (error) {
    console.error("Logout error:", error);
  }

  // Clear frontend state
  setUser(null);
  setJobs([]);
  setApplications([]);
  setStudentProfile(null);
  setEditingProfile(false);
  setProfileError("");

  setProfileForm({
    full_name: "",
    phone: "",
    city: "",
    state: "",
    country: "",
    qualification: "",
    degree_name: "",
    branch: "",
    college: "",
    graduation_year: "",
    cgpa: "",
    percentage: "",
  });

  setEmail("");
  setPassword("");
}

  // ==================================================
// VIEW JOB DETAILS
// ==================================================

async function handleViewJob(job) {
  setJobDetailsLoading(true);
  setApplicationMessage("");

  try {
    // ==================================================
    // EXTERNAL JOBS
    // Always fetch the latest data from the backend
    // ==================================================

    if (job.job_type === "external") {
      const externalJobId =
        job.job_id ?? job.id;

      const response = await fetch(
        `${API_URL}/external-jobs/${externalJobId}`,
        {
          method: "GET",
          credentials: "include",
          headers: {
            Accept: "application/json",
          },
        }
      );

      if (!response.ok) {
        throw new Error(
          `Unable to load external job: ${response.status}`
        );
      }

      const data = await response.json();

      // Keep external job information
      setSelectedJob({
        ...data,

        // Make sure frontend knows this is external
        job_id: data.id,
        job_type: "external",
      });

      return;
    }

    // ==================================================
    // INTERNAL JOBS
    // ==================================================

    const response = await fetch(
      `${API_URL}/jobs/${job.job_id}`,
      {
        method: "GET",
        credentials: "include",
        headers: {
          Accept: "application/json",
        },
      }
    );

    if (!response.ok) {
      throw new Error(
        `Unable to load job details: ${response.status}`
      );
    }

    const data = await response.json();

    setSelectedJob({
      ...data,
      job_id: data.id,
      job_type: "internal",
    });

  } catch (error) {
    console.error(
      "Job details error:",
      error
    );

    alert(
      error.message ||
      "Unable to load job details. Please try again."
    );

  } finally {
    setJobDetailsLoading(false);
  }
}


  // ==================================================
// APPLY FOR JOB
// ==================================================

async function handleApply(job) {
  if (!job || !job.job_id || !job.job_type) {
    setApplicationMessage("Unable to identify this job.");
    return;
  }

  // Prevent duplicate application from the frontend.
 const alreadyApplied = applications.some(
  (application) =>
    Number(application.job_id) === Number(job.job_id) &&
    application.job_type === job.job_type
);

  if (alreadyApplied) {
    setApplicationMessage(
      "You have already applied for this job."
    );
    return;
  }

  setApplying(true);
  setApplicationMessage("");

  const isExternal = job.job_type === "external";

  const companyName = isExternal
    ? job.company_name || "External Company"
    : `Company #${job.company_id}`;

  try {
    const response = await fetch(`${API_URL}/applications`, {
      method: "POST",
      credentials: "include",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },

      body: JSON.stringify({
        job_id: job.job_id,
        job_type: job.job_type,
        job_title: job.title,
        company_name: companyName,
        job_location: job.location,
        application_status: "Applied",

        notes: isExternal
          ? `External application through ${
              job.source || "job source"
            }`
          : "Applied through JobMatch AI",
      }),
    });

    const data = await response.json();

    if (!response.ok) {
      let message = "Unable to submit application.";

      if (typeof data.detail === "string") {
        message = data.detail;
      } else if (Array.isArray(data.detail)) {
        message = data.detail
          .map((item) => item.msg || "Invalid request")
          .join(", ");
      } else if (data.detail) {
        message = JSON.stringify(data.detail);
      }

      throw new Error(message);
    }

    // Refresh My Applications immediately.
    await loadApplications();

    setApplicationMessage(
      "Application recorded successfully."
    );

    // External jobs: open the original job posting.
    if (isExternal && job.application_url) {
      window.open(
        job.application_url,
        "_blank",
        "noopener,noreferrer"
      );
    }

    // Close the job popup after successful application.
    setSelectedJob(null);

  } catch (error) {
    console.error(
      "Apply error:",
      error
    );

    setApplicationMessage(
      error.message ||
        "Unable to submit application."
    );

  } finally {
    setApplying(false);
  }
}

 // ==================================================
// VIEW APPLICATION
// ==================================================

async function handleViewApplication(applicationId) {
  setApplicationActionLoading(true);

  try {
    const response = await fetch(
      `${API_URL}/applications/${applicationId}`,
      {
        method: "GET",
        credentials: "include",
        headers: {
          Accept: "application/json",
        },
      }
    );

    const data = await response.json();

    if (!response.ok) {
      throw new Error(
        typeof data.detail === "string"
          ? data.detail
          : "Unable to load application"
      );
    }

    setSelectedApplication(data);

  } catch (error) {
    console.error(
      "View application error:",
      error
    );

    alert(
      error.message ||
        "Unable to load application."
    );

  } finally {
    setApplicationActionLoading(false);
  }
}


// ==================================================
// OPEN JOB FROM APPLICATION
// ==================================================

async function handleOpenAppliedJob(application) {
  if (!application) {
    return;
  }

  if (!application.job_id || !application.job_type) {
    alert(
      "Job details are not available for this application."
    );
    return;
  }

  // ==================================================
  // EXTERNAL JOB
  // ==================================================

  if (application.job_type === "external") {
    try {
      const response = await fetch(
        `${API_URL}/external-jobs/${application.job_id}`,
        {
          method: "GET",
          credentials: "include",
          headers: {
            Accept: "application/json",
          },
        }
      );

      if (!response.ok) {
        throw new Error(
          `Unable to load external job: ${response.status}`
        );
      }

      const job = await response.json();

      if (job.application_url) {
        window.open(
          job.application_url,
          "_blank",
          "noopener,noreferrer"
        );
      } else {
        alert(
          "Original application link is not available."
        );
      }

    } catch (error) {
      console.error(
        "Open external job error:",
        error
      );

      alert(
        error.message ||
          "Unable to open the original job."
      );
    }

    return;
  }


  // ==================================================
  // INTERNAL JOB
  // ==================================================

  try {
    const response = await fetch(
      `${API_URL}/jobs/${application.job_id}`,
      {
        method: "GET",
        credentials: "include",
        headers: {
          Accept: "application/json",
        },
      }
    );

    if (!response.ok) {
      throw new Error(
        `Unable to load job: ${response.status}`
      );
    }

    const job = await response.json();

    setSelectedJob({
      ...job,
      job_id: job.id,
      job_type: "internal",
    });

  } catch (error) {
    console.error(
      "Open internal job error:",
      error
    );

    alert(
      error.message ||
        "Unable to open this job."
    );
  }
}

  // ==================================================
  // START EDITING APPLICATION
  // ==================================================

  function handleStartEdit(application) {
    setEditingApplication(application);
    setEditStatus(application.application_status || "Applied");
    setEditNotes(application.notes || "");
    setSelectedApplication(null);
  }

  // ==================================================
  // UPDATE APPLICATION
  // ==================================================

  async function handleUpdateApplication(event) {
    event.preventDefault();

    if (!editingApplication) {
      return;
    }

    setApplicationActionLoading(true);

    try {
      const response = await fetch(
        `${API_URL}/applications/${editingApplication.id}`,
        {
          method: "PUT",
          credentials: "include",
          headers: {
            Accept: "application/json",
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            application_status: editStatus,
            notes: editNotes,
          }),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || "Unable to update application"
        );
      }

      setEditingApplication(null);

      await loadApplications();

      alert("Application updated successfully!");
    } catch (error) {
      console.error("Update application error:", error);

      alert(
        error.message || "Unable to update application."
      );
    } finally {
      setApplicationActionLoading(false);
    }
  }

  // ==================================================
  // DELETE APPLICATION
  // ==================================================

  async function handleDeleteApplication(applicationId) {
    const confirmed = window.confirm(
      "Are you sure you want to delete this application?"
    );

    if (!confirmed) {
      return;
    }

    setApplicationActionLoading(true);

    try {
      const response = await fetch(
        `${API_URL}/applications/${applicationId}`,
        {
          method: "DELETE",
          credentials: "include",
          headers: {
            Accept: "application/json",
          },
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || "Unable to delete application"
        );
      }

      setSelectedApplication(null);
      setEditingApplication(null);

      await loadApplications();

      alert("Application deleted successfully!");
    } catch (error) {
      console.error("Delete application error:", error);

      alert(
        error.message || "Unable to delete application."
      );
    } finally {
      setApplicationActionLoading(false);
    }
  }

  // ==================================================
  // LOGIN SCREEN
  // ==================================================

if (checkingSession) {
  return (
    <div className="login-page">
      <h2>Checking session...</h2>
    </div>
  );
}


if (!user) {
    return (
      <div className="login-page">

        {/* Login card */}
        <div className="login-card">

          <div className="login-logo">
            <span className="logo-icon">J</span>
            <span>JobMatch AI</span>
          </div>

          <h1>Welcome Back</h1>

          <p className="login-subtitle">
            Login to see jobs matched to your profile.
          </p>

{showRegister ? (
  <form
    className="register-form"
    onSubmit={handleRegister}
  >

<div className="register-heading">
  <h2>Create Your Account</h2>
  <p>
    Join JobMatch AI and discover opportunities made for you.
  </p>
</div>

<label>Email</label>

<input
  type="email"
  value={registerEmail}
  onChange={(event) =>
    setRegisterEmail(event.target.value)
  }
  placeholder="Enter your email"
  required
/>

    <label>Password</label>

    <input
      type="password"
      value={registerPassword}
      onChange={(event) =>
        setRegisterPassword(event.target.value)
      }
      placeholder="Create a password"
      minLength={8}
      required
    />

<label>Account Type</label>

<div className="account-type-options">

  <button
    type="button"
    className={
      registerRole === "student"
        ? "account-type active"
        : "account-type"
    }
    onClick={() => setRegisterRole("student")}
  >
    <span className="account-type-icon">🎓</span>

    <span>
      <strong>Student</strong>
      <small>Find jobs matched to you</small>
    </span>
  </button>

  <button
    type="button"
    className={
      registerRole === "company"
        ? "account-type active"
        : "account-type"
    }
    onClick={() => setRegisterRole("company")}
  >
    <span className="account-type-icon">🏢</span>

    <span>
      <strong>Company</strong>
      <small>Find talented candidates</small>
    </span>
  </button>

</div>

    {registerError && (
      <div className="login-error">
        {registerError}
      </div>
    )}

    {registerMessage && (
      <div className="login-success">
        {registerMessage}
      </div>
    )}

<button
  className="login-button register-submit"
  type="submit"
  disabled={registering}
>
      {registering
        ? "Creating Account..."
        : "Create Account"}
    </button>

    <button
      type="button"
      className="register-back"
      onClick={() => {
        setShowRegister(false);
        setRegisterError("");
        setRegisterMessage("");
      }}
    >
      Back to Login
    </button>

  </form>
) : (
  <form onSubmit={handleLogin}>

    <label>Email</label>

    <input
      type="email"
      value={email}
      onChange={(event) =>
        setEmail(event.target.value)
      }
      placeholder="Enter your email"
      required
    />

    <label>Password</label>

    <input
      type="password"
      value={password}
      onChange={(event) =>
        setPassword(event.target.value)
      }
      placeholder="Enter your password"
      required
    />

    {loginError && (
      <div className="login-error">
        {loginError}
      </div>
    )}

    <button
      className="login-button"
      type="submit"
      disabled={loggingIn}
    >
      {loggingIn
        ? "Logging in..."
        : "Login"}
    </button>

    <button
      type="button"
      className="login-button"
      onClick={() => {
        setShowRegister(true);
        setRegisterError("");
        setRegisterMessage("");
      }}
    >
      Create Account
    </button>

  </form>
)}

        </div>
      </div>
    );
  }

  // ==================================================
  // COMPANY DASHBOARD
  // ==================================================

  if (user.role === "company") {
    return (
      <div className="app">

        {/* COMPANY HEADER */}

        <header className="header">

          <div className="logo">

            <span className="logo-icon">
              J
            </span>

            <span>
              JobMatch AI
            </span>

          </div>

          <nav>

            <a
              className="active"
              href="#company-dashboard"
            >
              Dashboard
            </a>

            <a href="#company-jobs">
              My Jobs
            </a>

            <a href="#company-applications">
              Applications
            </a>

          </nav>

          <div className="user">

            <div className="avatar">
              T
            </div>

            <div>

              <strong>
                Tech Solutions
              </strong>

              <small>
                Company
              </small>

            </div>

            <button
              className="logout-button"
              onClick={handleLogout}
            >
              Logout
            </button>

          </div>

        </header>


        {/* COMPANY MAIN */}

        <main className="container">

          {/* COMPANY WELCOME */}

          <section
            className="welcome"
            id="company-dashboard"
          >

            <div>

              <p className="welcome-label">
                COMPANY DASHBOARD
              </p>

              <h1>
                Welcome, Tech Solutions 👋
              </h1>

              <p>
                Manage your jobs and track applications
                from one place.
              </p>

            </div>


            <div className="profile-card">

              <div className="profile-avatar">
                T
              </div>

              <div>

                <strong>
                  Tech Solutions
                </strong>

                <span>
                  Software Development
                </span>

                <span>
                  Company ID: #2
                </span>

              </div>

            </div>

          </section>


          {/* COMPANY STATS */}

          <section className="stats-grid">

            <div className="stat-card">

              <div className="stat-icon blue">
                💼
              </div>

              <div>

                <span>
                  Active Jobs
                </span>

                <strong>
                  2
                </strong>

              </div>

            </div>


            <div className="stat-card">

              <div className="stat-icon green">
                👥
              </div>

              <div>

                <span>
                  Applications
                </span>

                <strong>
                  —
                </strong>

              </div>

            </div>


            <div className="stat-card">

              <div className="stat-icon orange">
                🏢
              </div>

              <div>

                <span>
                  Company ID
                </span>

                <strong>
                  #2
                </strong>

              </div>

            </div>

          </section>


          {/* MY JOBS */}

          <section
            className="jobs-section"
            id="company-jobs"
          >

            <div className="section-heading">

              <div>

                <h2>
                  My Jobs
                </h2>

                <p>
                  Jobs posted by Tech Solutions
                </p>

              </div>

            </div>


<div className="message">

  <h3>
    Your company jobs
  </h3>

  {loadingCompanyJobs && (
    <p>
      Loading your jobs...
    </p>
  )}

  {companyJobsError && !loadingCompanyJobs && (
    <p className="error">
      {companyJobsError}
    </p>
  )}

  {!loadingCompanyJobs &&
    !companyJobsError &&
    companyJobs.length === 0 && (
      <p>
        No jobs have been posted yet.
      </p>
    )}

  {!loadingCompanyJobs &&
    !companyJobsError &&
    companyJobs.map((job) => (
      <div
        key={job.id}
        className="company-job-item"
      >

        <h3>
          {job.title}
        </h3>

        <p>
          {job.description ||
            "No description available."}
        </p>

        <p>
          📍 {job.location ||
            "Location not specified"}
        </p>

        <p>
          💼 {job.employment_type ||
            "Employment type not specified"}
        </p>

        <p>
          🏠 {job.work_mode ||
            "Work mode not specified"}
        </p>

        <p>
          💰 ₹{job.salary_min || 0}
          {" - "}
          ₹{job.salary_max || 0}
        </p>

        <p>
          Status:{" "}
          <strong>
            {job.status}
          </strong>
        </p>

      </div>
    ))}

</div>

          </section>


          {/* APPLICATIONS */}

          <section
            className="jobs-section"
            id="company-applications"
          >

            <div className="section-heading">

              <div>

                <h2>
                  Applications
                </h2>

                <p>
                  Manage applications received for your jobs.
                </p>

              </div>

            </div>


<div className="company-applications">

  {loadingCompanyApplications && (
    <div className="message">
      <div className="spinner"></div>
      <p>Loading applications...</p>
    </div>
  )}

  {companyApplicationsError &&
    !loadingCompanyApplications && (
      <div className="message error">
        <h3>Unable to load applications</h3>
        <p>{companyApplicationsError}</p>
      </div>
    )}

  {!loadingCompanyApplications &&
    !companyApplicationsError &&
    companyApplications.length === 0 && (
      <div className="message">
        <h3>No applications yet</h3>
        <p>
          Applications received for your company jobs
          will appear here.
        </p>
      </div>
    )}

  {!loadingCompanyApplications &&
    !companyApplicationsError &&
    companyApplications.length > 0 && (

      <div className="company-applications-list">

        {companyApplications.map((application) => (

          <article
            className="company-application-card"
            key={application.id}
          >

            <div className="applicant-avatar">
              {(application.student_name || "S")
                .charAt(0)
                .toUpperCase()}
            </div>

            <div className="applicant-info">

              <h3>
                {application.student_name ||
                  "Student"}
              </h3>

              <p className="applicant-email">
                {application.student_email ||
                  "Email not available"}
              </p>

              <p className="applicant-job">
                Applied for:{" "}
                <strong>
                  {application.job_title}
                </strong>
              </p>

              <small>
                {application.job_location ||
                  "Location not specified"}
              </small>

            </div>

<div className="applicant-status">

  <span
    className={`application-status ${
      (application.application_status || "Applied")
        .toLowerCase()
        .replace(/\s+/g, "-")
    }`}
  >
    {application.application_status || "Applied"}
  </span>

  <select
    value={application.application_status || "Applied"}
    onChange={(event) =>
      handleCompanyApplicationStatus(
        application.id,
        event.target.value
      )
    }
  >
    <option value="Applied">
      Applied
    </option>

    <option value="Reviewing">
      Reviewing
    </option>

    <option value="Shortlisted">
      Shortlisted
    </option>

    <option value="Interview">
      Interview
    </option>

    <option value="Selected">
      Selected
    </option>

    <option value="Rejected">
      Rejected
    </option>
  </select>

  <small>
    {application.applied_at
      ? new Date(
          application.applied_at
        ).toLocaleDateString()
      : "Date not available"}
  </small>

</div>

          </article>

        ))}

      </div>

    )}

</div>

          </section>

        </main>

      </div>
    );
  }


  // ==================================================
  // STUDENT DASHBOARD
  // ==================================================
// ==================================================
// STUDENT DASHBOARD
// ==================================================

const filteredJobs = jobs.filter((job) => {
  const search = jobSearch.trim().toLowerCase();
  const location = jobLocationFilter.trim().toLowerCase();

  const matchesSearch =
    !search ||
    (job.title || "").toLowerCase().includes(search) ||
    (job.company_name || "").toLowerCase().includes(search);

  const matchesLocation =
    !location ||
    (job.location || "").toLowerCase().includes(location);

  const matchesWorkMode =
    !jobWorkModeFilter ||
    (job.work_mode || "").toLowerCase() ===
      jobWorkModeFilter.toLowerCase();

  const matchesEmployment =
    !jobEmploymentFilter ||
    (job.employment_type || "").toLowerCase() ===
      jobEmploymentFilter.toLowerCase();

  const matchesSource =
    !jobSourceFilter ||
    (job.source || "").toLowerCase() ===
      jobSourceFilter.toLowerCase();

  const matchesSalary =
    !jobMinSalaryFilter ||
    Number(job.salary_max || 0) >=
      Number(jobMinSalaryFilter);

  return (
    matchesSearch &&
    matchesLocation &&
    matchesWorkMode &&
    matchesEmployment &&
    matchesSource &&
    matchesSalary
  );
});

return (
  
    <div className="app">

      {/* HEADER */}

      <header className="header">

        <div className="logo">

          <span className="logo-icon">
            J
          </span>

          <span>
            JobMatch AI
          </span>

        </div>

        <nav>

          <a
            className="active"
            href="#dashboard"
          >
            Dashboard
          </a>

          <a href="#jobs">
            Jobs
          </a>

          <a href="#applications">
            Applications
          </a>

          <a href="#profile">
            Profile
          </a>

        </nav>

        <div className="user">

          <div className="avatar">
            B
          </div>

          <div>

            <strong>
  {studentProfile?.full_name || "Student"}
</strong>

<small>
  Student
</small>  

          </div>

          <button
            className="logout-button"
            onClick={handleLogout}
          >
            Logout
          </button>

        </div>

      </header>


      {/* MAIN */}

      <main className="container">

        {/* WELCOME */}

        <section
          className="welcome"
          id="dashboard"
        >

          <div>

            <p className="welcome-label">
              STUDENT DASHBOARD
            </p>

            <h1>
              Welcome back, {studentProfile?.full_name || "Student"}👋
            </h1>

            <p>
              Here are the jobs that best match
              your education, skills and preferences.
            </p>

          </div>

          <div className="profile-card">

            <div className="profile-avatar">
              B
            </div>

            <div>

              <strong>
  {studentProfile?.full_name || "Student"}
</strong>

<span>
  {studentEducation.length > 0
    ? (
        studentEducation[0].degree_name ||
        studentEducation[0].qualification ||
        "Education not specified"
      )
    : "Education not available"}
</span>

<span>
  {studentEducation.length > 0
    ? (
        studentEducation[0].branch
          ? `${studentEducation[0].branch}${
              studentProfile?.city
                ? ` • ${studentProfile.city}`
                : ""
            }`
          : studentProfile?.city || ""
      )
    : studentProfile?.city || ""}
</span>

            </div>

          </div>

        </section>


        {/* STATISTICS */}

        <section className="stats">

          <div className="stat-card">

            <div className="stat-icon blue">
              💼
            </div>

            <div>

              <span>
                Matching Jobs
              </span>

              <strong>
                {jobs.length}
              </strong>

            </div>

          </div>


          <div className="stat-card">

            <div className="stat-icon green">
              🎯
            </div>

            <div>

              <span>
                Best Match
              </span>

              <strong>
                {jobs.length > 0
                  ? `${jobs[0].match_score}%`
                  : "—"}
              </strong>

            </div>

          </div>


          <div className="stat-card">

            <div className="stat-icon purple">
              🛠️
            </div>

            <div>

              <span>
                Skills
              </span>

              <strong>
                {studentSkills.length}
              </strong>

            </div>

          </div>


          <div className="stat-card">

            <div className="stat-icon orange">
              📍
            </div>

            <div>

              <span>
                Preferred Location
              </span>

              <strong>
  {studentProfile?.city || "Not specified"}
</strong>

            </div>

          </div>

        </section>


        {/* PROFILE COMPLETION + QUICK ACTIONS */}

        <section className="dashboard-tools">

          {/* PROFILE COMPLETION */}

          <div className="completion-card">

            <div className="completion-header">

              <div>
                <span className="completion-label">
                  PROFILE COMPLETION
                </span>

                <h3>
                  Complete your profile
                </h3>

                <p>
                  A complete profile helps JobMatch AI
                  find better job matches for you.
                </p>
              </div>

              <div className="completion-percent">
                {Math.min(
                  100,
                  Math.round(
                    (
                      (studentProfile ? 2 : 0) +
                      (studentEducation.length > 0 ? 3 : 0) +
                      (studentSkills.length > 0 ? 3 : 0)
                    ) / 8 * 100
                  )
                )}%
              </div>

            </div>


            <div className="completion-progress">

              <div
                className="completion-progress-fill"
                style={{
                  width: `${Math.min(
                    100,
                    Math.round(
                      (
                        (studentProfile ? 2 : 0) +
                        (studentEducation.length > 0 ? 3 : 0) +
                        (studentSkills.length > 0 ? 3 : 0)
                      ) / 8 * 100
                    )
                  )}%`
                }}
              />

            </div>


            <div className="completion-footer">

              <span>
                {studentProfile
                  ? "✓ Personal details"
                  : "○ Personal details"}
              </span>

              <span>
                {studentEducation.length > 0
                  ? "✓ Education"
                  : "○ Education"}
              </span>

              <span>
                {studentSkills.length > 0
                  ? "✓ Skills"
                  : "○ Skills"}
              </span>

            </div>

          </div>


          {/* QUICK ACTIONS */}

          <div className="quick-actions-card">

            <div className="quick-actions-heading">

              <span className="completion-label">
                QUICK ACTIONS
              </span>

              <h3>
                What would you like to do?
              </h3>

            </div>


            <div className="quick-actions">

              <a
                href="#jobs"
                className="quick-action"
              >
                <span className="quick-action-icon">
                  💼
                </span>

                <span>
                  <strong>Browse Jobs</strong>
                  <small>
                    Explore matched opportunities
                  </small>
                </span>

                <b>→</b>
              </a>


              <a
                href="#applications"
                className="quick-action"
              >
                <span className="quick-action-icon">
                  📄
                </span>

                <span>
                  <strong>Applications</strong>
                  <small>
                    Track your applications
                  </small>
                </span>

                <b>→</b>
              </a>


              <a
                href="#profile"
                className="quick-action"
              >
                <span className="quick-action-icon">
                  👤
                </span>

                <span>
                  <strong>Edit Profile</strong>
                  <small>
                    Keep your profile updated
                  </small>
                </span>

                <b>→</b>
              </a>

            </div>

          </div>

        </section>


        {/* RECOMMENDED JOBS */}

        <section
          className="jobs-section"
          id="jobs"
        >

          <div className="section-heading">

            <div>

              <h2>
                Recommended Jobs
              </h2>

              <p>
                Jobs ranked according to your profile
              </p>

            </div>

            <button
              className="refresh-button"
              onClick={loadJobs}
              disabled={loadingJobs}
            >
              {loadingJobs
                ? "Loading..."
                : "↻ Refresh"}
            </button>

                    </div>

          <div className="job-filters">

            <input
              type="text"
              placeholder="Search jobs or companies..."
              value={jobSearch}
              onChange={(e) =>
                setJobSearch(e.target.value)
              }
            />

            <input
              type="text"
              placeholder="Location..."
              value={jobLocationFilter}
              onChange={(e) =>
                setJobLocationFilter(e.target.value)
              }
            />

            <select
              value={jobWorkModeFilter}
              onChange={(e) =>
                setJobWorkModeFilter(e.target.value)
              }
            >
              <option value="">All Work Modes</option>
              <option value="Remote">Remote</option>
              <option value="Hybrid">Hybrid</option>
              <option value="On-site">On-site</option>
            </select>

            <select
              value={jobEmploymentFilter}
              onChange={(e) =>
                setJobEmploymentFilter(e.target.value)
              }
            >
              <option value="">All Employment Types</option>
              <option value="Full-time">Full-time</option>
              <option value="Part-time">Part-time</option>
              <option value="Internship">Internship</option>
              <option value="Contract">Contract</option>
            </select>

            <select
              value={jobSourceFilter}
              onChange={(e) =>
                setJobSourceFilter(e.target.value)
              }
            >
<option value="">All Sources</option>
<option value="Jooble">Jooble</option>
<option value="Adzuna">Adzuna</option>
<option value="JobDataLake">JobDataLake</option>
            </select>

            <select
              value={jobMinSalaryFilter}
              onChange={(e) =>
                setJobMinSalaryFilter(e.target.value)
              }
            >
              <option value="">Any Salary</option>
              <option value="200000">₹2 LPA+</option>
              <option value="300000">₹3 LPA+</option>
              <option value="500000">₹5 LPA+</option>
              <option value="800000">₹8 LPA+</option>
            </select>

            <button
              type="button"
              onClick={() => {
                setJobSearch("");
                setJobLocationFilter("");
                setJobWorkModeFilter("");
                setJobEmploymentFilter("");
                setJobSourceFilter("");
                setJobMinSalaryFilter("");
              }}
            >
              Clear Filters
            </button>

          </div>


          {loadingJobs && ( 

            <div className="message">

              <div className="spinner"></div>

              <p>
                Finding the best jobs for you...
              </p>

            </div>

          )}


          {jobsError && !loadingJobs && (

            <div className="message error">

              <h3>
                Something went wrong
              </h3>

              <p>
                {jobsError}
              </p>

            </div>

          )}


          {!loadingJobs &&
            !jobsError &&
            jobs.length === 0 && (

              <div className="message">

                <h3>
                  No matching jobs found
                </h3>

                <p>
                  Try updating your profile or preferences.
                </p>

              </div>

            )}


          {!loadingJobs &&
            !jobsError &&
            jobs.length > 0 && (

              <div className="jobs-list">

                {filteredJobs.map((job) => {
  const alreadyApplied = applications.some(
    (application) =>
      Number(application.job_id) === Number(job.job_id) &&
      application.job_type === job.job_type
  );

  return (
    <article
      className="job-card"
      key={`${job.job_type}-${job.job_id}`}
    >

      <div className="job-top">

        <div className="company-logo">
          {job.title.charAt(0)}
        </div>

        <div className="job-title-area">

          <h3>
            {job.title}
          </h3>

          <p>
            {job.job_type === "external"
              ? job.company_name || "External Company"
              : `Company #${job.company_id}`}
          </p>

        </div>

        <div
          className={`match-badge ${
            job.match_score >= 90
              ? "excellent"
              : job.match_score >= 70
              ? "good"
              : "average"
          }`}
        >
          {job.match_score}% Match
        </div>

      </div>


      <div className="job-details">

        <span>
          📍 {job.location || "Location not specified"}
        </span>

        <span>
          💻 {job.work_mode || "Work mode not specified"}
        </span>

        <span>
          💰{" "}
          {job.salary_min != null || job.salary_max != null
            ? `₹${
                job.salary_min != null
                  ? (job.salary_min / 100000).toFixed(1)
                  : "—"
              }L - ₹${
                job.salary_max != null
                  ? (job.salary_max / 100000).toFixed(1)
                  : "—"
              }L`
            : "Salary not specified"}
        </span>

      </div>


      <div className="reasons">

        <h4>
          Why this job matches you
        </h4>

<div className="reason-list">

  {job.reasons.map(
    (reason, index) => {

      const reasonText = String(
        reason || ""
      );

      const isNegative =
        reasonText.toLowerCase().includes(
          "does not match"
        ) ||
        reasonText.toLowerCase().includes(
          "does not meet"
        ) ||
        reasonText.toLowerCase().includes(
          "not met"
        ) ||
        reasonText.toLowerCase().includes(
          "requires experience"
        );

      const isNeutral =
        reasonText.toLowerCase().includes(
          "not specified"
        ) ||
        reasonText.toLowerCase().includes(
          "no detected"
        ) ||
        reasonText.toLowerCase().includes(
          "no work mode preference"
        ) ||
        reasonText.toLowerCase().includes(
          "no employment type preference"
        ) ||
        reasonText.toLowerCase().includes(
          "not directly match"
        );

      return (
        <span
          key={index}
          className={
            `reason ${
              isNegative
                ? "reason-negative"
                : isNeutral
                ? "reason-neutral"
                : "reason-positive"
            }`
          }
        >

          {isNegative
            ? "✕"
            : isNeutral
            ? "•"
            : "✓"}

          {" "}

          {reasonText}

        </span>
      );

    }
  )}

</div>

      </div>


      <div className="job-footer">

        <span className="job-id">
          {job.job_type === "external"
            ? `Source: ${job.source || "External"}`
            : `Job ID: #${job.job_id}`}
        </span>

        <button
          className="apply-button"
          onClick={() => handleViewJob(job)}
          disabled={jobDetailsLoading}
        >
          {jobDetailsLoading
            ? "Loading..."
            : alreadyApplied
            ? "✓ Applied"
            : "View Job →"}
        </button>

      </div>

    </article>
  );
})}

              </div>

            )}

        </section>


        {/* MY APPLICATIONS */}

        <section
          className="applications-section"
          id="applications"
        >

          <div className="section-heading">

            <div>

              <h2>
                My Applications
              </h2>

              <p>
                Jobs you have applied for
              </p>

            </div>

            <button
              className="refresh-button"
              onClick={loadApplications}
              disabled={loadingApplications}
            >
              {loadingApplications
                ? "Loading..."
                : "↻ Refresh"}
            </button>

          </div>


          <div className="application-summary">

  <div className="application-count">
    <span>
      Total Applications
    </span>

    <strong>
      {applications.length}
    </strong>
  </div>


  <div className="application-count">
    <span>
      Applied
    </span>

    <strong>
      {
        applications.filter(
          (application) =>
            application.application_status === "Applied"
        ).length
      }
    </strong>
  </div>


  <div className="application-count">
    <span>
      Shortlisted
    </span>

    <strong>
      {
        applications.filter(
          (application) =>
            application.application_status === "Shortlisted"
        ).length
      }
    </strong>
  </div>


  <div className="application-count">
    <span>
      Interview
    </span>

    <strong>
      {
        applications.filter(
          (application) =>
            application.application_status === "Interview"
        ).length
      }
    </strong>
  </div>


  <div className="application-count">
    <span>
      Selected
    </span>

    <strong>
      {
        applications.filter(
          (application) =>
            application.application_status === "Selected"
        ).length
      }
    </strong>
  </div>


  <div className="application-count">
    <span>
      Rejected
    </span>

    <strong>
      {
        applications.filter(
          (application) =>
            application.application_status === "Rejected"
        ).length
      }
    </strong>
  </div>

</div>


          {applicationsError && (

            <div className="message error">

              <h3>
                Something went wrong
              </h3>

              <p>
                {applicationsError}
              </p>

            </div>

          )}


          {loadingApplications && (

            <div className="message">

              <div className="spinner"></div>

              <p>
                Loading your applications...
              </p>

            </div>

          )}


          {!loadingApplications &&
            !applicationsError &&
            applications.length === 0 && (

              <div className="message">

                <h3>
                  No applications yet
                </h3>

                <p>
                  Apply for a recommended job and
                  it will appear here.
                </p>

              </div>

            )}


          {!loadingApplications &&
            !applicationsError &&
            applications.length > 0 && (

              <div className="applications-list">

                {applications.map(
                  (application) => (

                    <article
                      className="application-card"
                      key={application.id}
                    >

                      <div className="application-icon">
                        📄
                      </div>


                      <div className="application-info">

                        <h3>
                          {application.job_title}
                        </h3>

                        <p>
                          {application.company_name}
                        </p>

                        <span>
                          📍{" "}
                          {application.job_location ||
                            "Location not specified"}
                        </span>

                      </div>


                      <div className="application-status-area">

                        <span
                          className={`application-status ${
                            application.application_status
                              .toLowerCase()
                              .replace(/\s+/g, "-")
                          }`}
                        >
                          {application.application_status}
                        </span>

                        <small>
                          Application #{application.id}
                        </small>

                      </div>


                      <div className="application-buttons">

  {application.job_id &&
    application.job_type && (
      <button
        className="view-application-button"
        onClick={() =>
          handleOpenAppliedJob(application)
        }
        disabled={applicationActionLoading}
      >
        🔗 Open Job
      </button>
    )}

  <button
    className="view-application-button"
    onClick={() =>
      handleViewApplication(
        application.id
      )
    }
    disabled={
      applicationActionLoading
    }
  >
    👁 View
  </button>

  <button
    className="edit-application-button"
    onClick={() =>
      handleStartEdit(application)
    }
    disabled={
      applicationActionLoading
    }
  >
    ✏ Edit
  </button>

  <button
    className="delete-application-button"
    onClick={() =>
      handleDeleteApplication(
        application.id
      )
    }
    disabled={
      applicationActionLoading
    }
  >
    🗑 Delete
  </button>

</div>

                    </article>

                  )
                )}

              </div>

            )}

        </section>


        {/* PROFILE */}

        <section
          id="profile"
          className="profile-section"
        >

          <div className="section-heading">

            <div>

              <h2>
                My Profile
              </h2>

              <p>
                Your profile information
              </p>

            </div>

          </div>

          <div className="profile-display-card">

  <div className="profile-avatar large">
    {studentProfile?.full_name
      ? studentProfile.full_name
          .charAt(0)
          .toUpperCase()
      : "B"}
  </div>

  {!editingProfile ? (
    <div className="profile-display-content">

      <h3>
        {studentProfile?.full_name ||
          "Profile name not available"}
      </h3>

      {loadingEducation ? (
  <p>
    Loading education...
  </p>
) : educationError ? (
  <p>
    {educationError}
  </p>
) : studentEducation.length > 0 ? (
  <>
    <p>
      {studentEducation[0].degree_name ||
        studentEducation[0].qualification ||
        "Education not specified"}
    </p>

    {studentEducation[0].branch && (
      <p>
        {studentEducation[0].branch}
        {studentProfile?.city
          ? ` • ${studentProfile.city}`
          : ""}
      </p>
    )}

    {studentEducation[0].college && (
      <p>
        🎓 {studentEducation[0].college}
      </p>
    )}

    {studentEducation[0].graduation_year && (
      <p>
        Graduation Year:{" "}
        {studentEducation[0].graduation_year}
      </p>
    )}

    {studentEducation[0].cgpa != null && (
      <p>
        CGPA: {studentEducation[0].cgpa}
      </p>
    )}

    {studentEducation[0].percentage != null && (
      <p>
        Percentage: {studentEducation[0].percentage}%
      </p>
    )}
  </>
) : (
  <p>
    Education information not available
  </p>
)}


      {studentProfile?.phone && (
        <p>
          📞 {studentProfile.phone}
        </p>
      )}

      {studentProfile?.state && (
        <p>
          State: {studentProfile.state}
        </p>
      )}

      {studentProfile?.country && (
        <p>
          Country: {studentProfile.country}
        </p>
      )}

      {studentProfile?.id && (
        <p>
          Student ID: {studentProfile.id}
        </p>
      )}

      <button
  type="button"
  className="edit-profile-button"
  onClick={async () => {
    try {
      const response = await fetch(
        `${API_URL}/profile/education`,
        {
          method: "GET",
          credentials: "include",
          headers: {
            Accept: "application/json",
          },
        }
      );

      const educationData =
        await response.json();

      if (!response.ok) {
        throw new Error(
          "Unable to load education information."
        );
      }

      const education =
        Array.isArray(educationData)
          ? educationData[0]
          : null;

      setProfileForm({
        full_name:
          studentProfile?.full_name || "",
        phone:
          studentProfile?.phone || "",
        city:
          studentProfile?.city || "",
        state:
          studentProfile?.state || "",
        country:
          studentProfile?.country || "",

        qualification:
          education?.qualification || "",
        degree_name:
          education?.degree_name || "",
        branch:
          education?.branch || "",
        college:
          education?.college || "",
        graduation_year:
          education?.graduation_year || "",
        cgpa:
          education?.cgpa ?? "",
        percentage:
          education?.percentage ?? "",
      });

      setEditingProfile(true);

    } catch (error) {
      console.error(
        "Education loading error:",
        error
      );

      setProfileError(
        "Unable to load education information."
      );
    }
  }}
>
  Edit Profile
</button>

    </div>
  ) : (

    <form
      className="profile-edit-form"
      onSubmit={handleUpdateProfile}
    >

      <h3>
        Edit Profile
      </h3>

      {profileError && (
        <div className="message error">
          <p>{profileError}</p>
        </div>
      )}

      <label>
        Full Name
      </label>

      <input
        type="text"
        value={profileForm.full_name}
        onChange={(event) =>
          setProfileForm({
            ...profileForm,
            full_name: event.target.value,
          })
        }
        required
      />

      <label>
        Phone
      </label>

      <input
        type="text"
        value={profileForm.phone}
        onChange={(event) =>
          setProfileForm({
            ...profileForm,
            phone: event.target.value,
          })
        }
      />

      <label>
        City
      </label>

      <input
        type="text"
        value={profileForm.city}
        onChange={(event) =>
          setProfileForm({
            ...profileForm,
            city: event.target.value,
          })
        }
      />

      <label>
        State
      </label>

      <input
        type="text"
        value={profileForm.state}
        onChange={(event) =>
          setProfileForm({
            ...profileForm,
            state: event.target.value,
          })
        }
      />

      <label>
        Country
      </label>

      <input
        type="text"
        value={profileForm.country}
        onChange={(event) =>
          setProfileForm({
            ...profileForm,
            country: event.target.value,
          })
        }
      />

      
        <label>
  Qualification
</label>

<input
  type="text"
  value={profileForm.qualification}
  onChange={(event) =>
    setProfileForm({
      ...profileForm,
      qualification: event.target.value,
    })
  }
/>

<label>
  Degree Name
</label>

<input
  type="text"
  value={profileForm.degree_name}
  onChange={(event) =>
    setProfileForm({
      ...profileForm,
      degree_name: event.target.value,
    })
  }
/>

<label>
  Branch
</label>

<input
  type="text"
  value={profileForm.branch}
  onChange={(event) =>
    setProfileForm({
      ...profileForm,
      branch: event.target.value,
    })
  }
/>

<label>
  College
</label>

<input
  type="text"
  value={profileForm.college}
  onChange={(event) =>
    setProfileForm({
      ...profileForm,
      college: event.target.value,
    })
  }
/>

<label>
  Graduation Year
</label>

<input
  type="number"
  value={profileForm.graduation_year}
  onChange={(event) =>
    setProfileForm({
      ...profileForm,
      graduation_year: event.target.value,
    })
  }
/>

<label>
  CGPA
</label>

<input
  type="number"
  step="0.01"
  value={profileForm.cgpa}
  onChange={(event) =>
    setProfileForm({
      ...profileForm,
      cgpa: event.target.value,
    })
  }
/>

<label>
  Percentage
</label>

<input
  type="number"
  step="0.01"
  value={profileForm.percentage}
  onChange={(event) =>
    setProfileForm({
      ...profileForm,
      percentage: event.target.value,
    })
  }
/>
<div className="profile-edit-buttons">
        <button
          type="submit"
          className="save-profile-button"
          disabled={savingProfile}
        >
          {savingProfile
            ? "Saving..."
            : "Save Changes"}
        </button>

        <button
          type="button"
          className="cancel-profile-button"
          onClick={() =>
            setEditingProfile(false)
          }
          disabled={savingProfile}
        >
          Cancel
        </button>

      </div>

    </form>
  )}

</div>

          {/* STUDENT SKILLS */}

          <div className="profile-skills-card">

            <div className="profile-skills-heading">
              <div>
                <h3>Your Skills</h3>
                <p>
                  Add your actual skills so JobMatch AI can
                  calculate more accurate job matches.
                </p>
              </div>

              <span className="skill-count-badge">
                {studentSkills.length} Skills
              </span>
            </div>

            {skillsError && (
              <div className="message error">
                <p>{skillsError}</p>
              </div>
            )}
{loadingSkills ? (
  <div className="message">
    <div className="spinner"></div>
    <p>Loading skills...</p>
  </div>
) : (
  <>
    <div className="student-skills-list">
      {studentSkills.length === 0 ? (
        <div className="skills-empty">
          <p>No skills added yet. Add your skills below.</p>
        </div>
      ) : (
        studentSkills.map((skill) => (
          <div
            className="student-skill-chip"
            key={skill.id}
          >
            <div
              className="skill-info"
              style={{
                display: "flex",
                alignItems: "center",
                gap: "16px",
                flexWrap: "wrap",
              }}
            >
              <strong
                style={{
                  display: "inline-block",
                  marginRight: "4px",
                }}
              >
                {skill.canonical_name}
              </strong>

              {skill.category && (
                <span
                  className="skill-category"
                  style={{
                    display: "inline-block",
                    marginRight: "4px",
                  }}
                >
                  {skill.category}
                </span>
              )}

              {skill.proficiency && (
                <span
                  className="skill-proficiency"
                  style={{
                    display: "inline-block",
                    marginLeft: "4px",
                  }}
                >
                  Proficiency: {skill.proficiency}
                </span>
              )}
            </div>

            <button
              type="button"
              className="remove-skill-button"
              onClick={() =>
                handleRemoveSkill(skill.skill_id)
              }
              disabled={savingSkill}
              title={`Remove ${skill.canonical_name}`}
            >
              ×
            </button>
          </div>
        ))
      )}
    </div>
                <form
                  className="add-skill-form"
                  onSubmit={handleAddSkill}
                >
                  <div className="skill-form-field">
                    <label>Add a skill</label>

                    <select
                      value={selectedSkillId}
                      onChange={(event) =>
                        setSelectedSkillId(event.target.value)
                      }
                      disabled={savingSkill}
                    >
                      <option value="">Select a skill</option>

                      {allSkills
                        .filter(
                          (skill) =>
                            !studentSkills.some(
                              (studentSkill) =>
                                studentSkill.skill_id === skill.id
                            )
                        )
                        .map((skill) => (
                          <option key={skill.id} value={skill.id}>
                            {skill.canonical_name}
                            {skill.category
                              ? ` — ${skill.category}`
                              : ""}
                          </option>
                        ))}
                    </select>
                  </div>

                  <div className="skill-form-field">
                    <label>Proficiency</label>

                    <select
                      value={skillProficiency}
                      onChange={(event) =>
                        setSkillProficiency(event.target.value)
                      }
                      disabled={savingSkill}
                    >
                      <option value="">
                        Select proficiency
                      </option>

                      <option value="Beginner">
                        Beginner
                      </option>

                      <option value="Intermediate">
                        Intermediate
                      </option>

                      <option value="Advanced">
                        Advanced
                      </option>

                      <option value="Expert">
                        Expert
                      </option>
                    </select>
                  </div>

                  <button
                    type="submit"
                    className="add-skill-button"
                    disabled={savingSkill || !selectedSkillId}
                  >
                    {savingSkill ? "Saving..." : "+ Add Skill"}
                  </button>
                </form>
              </>
            )}
          </div>

        </section>

      </main>


      {/* ==================================================
          JOB DETAILS POPUP
          ================================================== */}

      {selectedJob && (

        <div
          className="modal-overlay"
          onClick={() =>
            setSelectedJob(null)
          }
        >

          <div
            className="job-modal"
            onClick={(event) =>
              event.stopPropagation()
            }
          >

            <button
              className="modal-close"
              onClick={() =>
                setSelectedJob(null)
              }
            >
              ×
            </button>


            <h2>
              {selectedJob.title}
            </h2>

            <p className="modal-company">
              {selectedJob.job_type === "external"
                ? selectedJob.company_name || "External Company"
                : `Company #${selectedJob.company_id}`}
            </p>
{/* AI MATCH SCORE */}

<div className="ai-match-card">

  <div className="ai-match-header">

    <div>
      <span className="ai-match-label">
        AI JOB MATCH
      </span>

      <h3>
        Why this job is recommended for you
      </h3>
    </div>

    <div className="ai-match-score">
      <strong>
        {selectedJob.match_score || 0}%
      </strong>

      <span>
        Match
      </span>
    </div>

  </div>


  <div className="ai-match-progress">

    <div
      className="ai-match-progress-fill"
      style={{
        width: `${selectedJob.match_score || 0}%`
      }}
    />

  </div>


  <div className="ai-match-status">

    <span className="ai-match-dot"></span>

    {selectedJob.match_score >= 90
      ? "Excellent match for your profile"
      : selectedJob.match_score >= 70
      ? "Strong match for your profile"
      : selectedJob.match_score >= 50
      ? "Good potential match"
      : "Some requirements may not match"}

  </div>

</div>


{/* MATCH REASONS */}

{selectedJob.reasons &&
  selectedJob.reasons.length > 0 && (

    <div className="match-reasons-modal">

      <h3>
        ✨ Match Breakdown
      </h3>

      <div className="modal-reason-list">

        {selectedJob.reasons.map(
          (reason, index) => {

            const reasonText =
              String(reason || "");

            const lower =
              reasonText.toLowerCase();

            const isNegative =
              lower.includes("does not match") ||
              lower.includes("does not meet") ||
              lower.includes("not met") ||
              lower.includes("requires experience");

            const isNeutral =
              lower.includes("not specified") ||
              lower.includes("no detected") ||
              lower.includes("not directly match") ||
              lower.includes("not restricted");

            return (
              <div
                key={index}
                className={
                  `modal-reason ${
                    isNegative
                      ? "negative"
                      : isNeutral
                      ? "neutral"
                      : "positive"
                  }`
                }
              >

                <span className="modal-reason-icon">

                  {isNegative
                    ? "×"
                    : isNeutral
                    ? "•"
                    : "✓"}

                </span>

                <span>
                  {reasonText}
                </span>

              </div>
            );

          }
        )}

      </div>

    </div>

  )}

            <div className="modal-details">

              <p>
                📍 <strong>Location:</strong>{" "}
                {selectedJob.location || "Not specified"}
              </p>

              <p>
                💻 <strong>Work Mode:</strong>{" "}
                {selectedJob.work_mode || "Not specified"}
              </p>

              <p>
                💰 <strong>Salary:</strong>{" "}
                {selectedJob.salary_min != null ||
                selectedJob.salary_max != null
                  ? `₹${
                      selectedJob.salary_min != null
                        ? (selectedJob.salary_min / 100000).toFixed(1)
                        : "—"
                    }L - ₹${
                      selectedJob.salary_max != null
                        ? (selectedJob.salary_max / 100000).toFixed(1)
                        : "—"
                    }L`
                  : "Not specified"}
              </p>

              <p>
                📋 <strong>Employment Type:</strong>{" "}
                {selectedJob.employment_type || "Not specified"}
              </p>

              {selectedJob.job_type === "external" ? (
                <p>
                  🌐 <strong>Source:</strong>{" "}
                  {selectedJob.source || "External"}
                </p>
              ) : (
                <p>
                  🆔 <strong>Job ID:</strong>{" "}
                  #{selectedJob.id}
                </p>
              )}

            </div>


<div className="modal-section">

  <h3>
    Job Description
  </h3>

  <div
    className="job-description"
    dangerouslySetInnerHTML={{
      __html:
        selectedJob.description ||
        "<p>No job description available.</p>"
    }}
  />

</div>


            {selectedJob.job_type !== "external" && (
              <div className="modal-section">

                <h3>
                  Responsibilities
                </h3>

                <p>
                  {selectedJob.responsibilities ||
                    "No responsibilities provided."}
                </p>

              </div>
            )}


            <div className="modal-section">

              <h3>
                Required Skills
              </h3>

              <div className="modal-skills">

                {selectedJob.required_skills &&
                selectedJob.required_skills.length > 0 ? (

                  selectedJob.required_skills.map(
                    (skill, index) => (

                      <span key={index}>
                        {skill}
                      </span>

                    )
                  )

                ) : (

                  <span>
                    No required skills listed
                  </span>

                )}

              </div>

            </div>


            {selectedJob.preferred_skills &&
              selectedJob.preferred_skills.length > 0 && (

                <div className="modal-section">

                  <h3>
                    Preferred Skills
                  </h3>

                  <div className="modal-skills">

                    {selectedJob.preferred_skills.map(
                      (skill, index) => (

                        <span key={index}>
                          {skill}
                        </span>

                      )
                    )}

                  </div>

                </div>

              )}


            <div className="modal-section">

              <h3>
                Education Requirement
              </h3>

              <p>
                {selectedJob.education_requirement ||
                  "Not specified"}
              </p>

            </div>


            <div className="modal-section">

              <h3>
                Application Deadline
              </h3>

              <p>
                {selectedJob.application_deadline ||
                  "Not specified"}
              </p>

            </div>


            {selectedJob.job_type === "external" &&
              selectedJob.application_url && (
                <div className="modal-section">
                  <h3>
                    Original Job Posting
                  </h3>

                  <p>
                    This job was collected from{" "}
                    {selectedJob.source || "an external source"}.
                    Clicking Apply will record your application
                    and open the original application page.
                  </p>
                </div>
              )}

            <div className="modal-actions">

  {selectedJob.job_type === "external" &&
    selectedJob.application_url && (

      <button
        className="secondary-button"
        onClick={() =>
          window.open(
            selectedJob.application_url,
            "_blank",
            "noopener,noreferrer"
          )
        }
      >
        View Full Job →
      </button>

  )}

  <button
    className="apply-button"
    onClick={() =>
      handleApply(selectedJob)
    }
    disabled={applying}
  >
    {applying
      ? "Applying..."
      : selectedJob.job_type === "external"
      ? "Apply & Record Application →"
      : "Apply for Job →"}
  </button>

  <button
    className="close-button"
    onClick={() =>
      setSelectedJob(null)
    }
  >
    Close
  </button>

</div>

            {applicationMessage && (

              <p className="application-message">
                {applicationMessage}
              </p>

            )}

          </div>

        </div>

      )}


      {/* ==================================================
          VIEW APPLICATION POPUP
          ================================================== */}

      {selectedApplication && (

        <div
          className="modal-overlay"
          onClick={() =>
            setSelectedApplication(null)
          }
        >

          <div
            className="application-modal"
            onClick={(event) =>
              event.stopPropagation()
            }
          >

            <button
              className="modal-close"
              onClick={() =>
                setSelectedApplication(null)
              }
            >
              ×
            </button>


            <div className="application-modal-icon">
              📄
            </div>

            <h2>
              {selectedApplication.job_title}
            </h2>

            <p className="modal-company">
              {selectedApplication.company_name}
            </p>


            <div className="application-detail-box">

              <div className="detail-row">

                <strong>
                  Application ID
                </strong>

                <span>
                  #{selectedApplication.id}
                </span>

              </div>
<div className="detail-row">
  <strong>
    Job ID
  </strong>

  <span>
    {selectedApplication.job_id
      ? `#${selectedApplication.job_id}`
      : "Not available"}
  </span>
</div>

<div className="detail-row">
  <strong>
    Job Type
  </strong>

  <span>
    {selectedApplication.job_type
      ? selectedApplication.job_type === "external"
        ? "External / Jooble"
        : "Internal"
      : "Not available"}
  </span>
</div>

              <div className="detail-row">

                <strong>
                  Location
                </strong>

                <span>
                  {selectedApplication.job_location ||
                    "Not specified"}
                </span>

              </div>


              <div className="detail-row">

                <strong>
                  Status
                </strong>

                <span className="application-status">
                  {selectedApplication.application_status}
                </span>

              </div>


              <div className="detail-row">

                <strong>
                  Applied At
                </strong>

                <span>
                  {selectedApplication.applied_at
                    ? new Date(
                        selectedApplication.applied_at
                      ).toLocaleString()
                    : "Not recorded"}
                </span>

              </div>

            </div>


            <div className="modal-section">

              <h3>
                Notes
              </h3>

              <p>
                {selectedApplication.notes ||
                  "No notes added."}
              </p>

            </div>


            <div className="modal-actions">

              <button
                className="edit-application-button large"
                onClick={() =>
                  handleStartEdit(
                    selectedApplication
                  )
                }
              >
                ✏ Edit Application
              </button>


              <button
                className="delete-application-button large"
                onClick={() =>
                  handleDeleteApplication(
                    selectedApplication.id
                  )
                }
              >
                🗑 Delete
              </button>

            </div>

          </div>

        </div>

      )}


      {/* ==================================================
          EDIT APPLICATION POPUP
          ================================================== */}

      {editingApplication && (

        <div
          className="modal-overlay"
          onClick={() =>
            setEditingApplication(null)
          }
        >

          <div
            className="edit-application-modal"
            onClick={(event) =>
              event.stopPropagation()
            }
          >

            <button
              className="modal-close"
              onClick={() =>
                setEditingApplication(null)
              }
            >
              ×
            </button>


            <h2>
              Edit Application
            </h2>

            <p className="modal-company">
              {editingApplication.job_title}
            </p>


            <form
              onSubmit={handleUpdateApplication}
              className="edit-form"
            >

              <label>
                Application Status
              </label>

              <select
                value={editStatus}
                onChange={(event) =>
                  setEditStatus(event.target.value)
                }
              >

                <option value="Applied">
                  Applied
                </option>

                <option value="Shortlisted">
                  Shortlisted
                </option>

                <option value="Interview">
                  Interview
                </option>

                <option value="Selected">
                  Selected
                </option>

                <option value="Rejected">
                  Rejected
                </option>

              </select>


              <label>
                Notes
              </label>

              <textarea
                value={editNotes}
                onChange={(event) =>
                  setEditNotes(event.target.value)
                }
                placeholder="Add notes about this application..."
                rows="6"
              />


              <div className="modal-actions">

                <button
                  type="submit"
                  className="apply-button"
                  disabled={applicationActionLoading}
                >
                  {applicationActionLoading
                    ? "Saving..."
                    : "Save Changes"}
                </button>


                <button
                  type="button"
                  className="close-button"
                  onClick={() =>
                    setEditingApplication(null)
                  }
                >
                  Cancel
                </button>

              </div>

            </form>

          </div>

        </div>

      )}

    </div>
  );
}

export default App;
