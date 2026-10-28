import React, { useState, useEffect, useMemo } from 'react';
import './App.css';
import { useTheme } from './utils/theme';
import { AuthProvider, useAuth, parseJwtPayload } from './context/AuthContext';

import LandingPageView from './components/LandingPageView';
import LoginModal from './components/LoginModal';
import Sidebar from './components/Sidebar';
import DashboardView from './components/DashboardView';
import ProfileView from './components/ProfileView';
import JobsView from './components/JobsView';
import ApplicationStudio from './components/ApplicationStudio';
import PipelineView from './components/PipelineView';
import InterviewCoachView from './components/InterviewCoachView';
import AdminView from './components/AdminView';
import JobDetailModal from './components/JobDetailModal';
import FollowUpModal from './components/FollowUpModal';
import MaterialsModal from './components/MaterialsModal';
import CommandPalette from './components/CommandPalette';
import Toast from './components/Toast';

const DEFAULT_ACCOUNT_ID = '6e488188-0015-4657-94c9-92d01413dcfb';
const API_BASE = '/api/v1';

function CareerAppInner() {
  const {
    user,
    token,
    authHeaders,
    logout,
    impersonateTenant,
    exitImpersonation,
    isImpersonating,
    impersonatedTenant,
    isSuperadmin,
  } = useAuth();

  const [accountId, setAccountId] = useState(() => {
    if (typeof window !== 'undefined') {
      const stored = localStorage.getItem('jobeazy_jwt_token');
      const parsed = parseJwtPayload(stored);
      if (parsed?.role === 'superadmin') return parsed.id;
      if (parsed?.id) return parsed.id;
    }
    return DEFAULT_ACCOUNT_ID;
  });

  const [activeSection, setActiveSectionState] = useState(() => {
    if (typeof window === 'undefined') return 'dashboard';
    const stored = localStorage.getItem('jobeazy_jwt_token');
    const parsed = parseJwtPayload(stored);
    const saved = localStorage.getItem('jobeazy_active_section');
    if (parsed?.role === 'superadmin') {
      return (saved && saved !== 'dashboard') ? saved : 'admin';
    }
    return (saved && saved !== 'admin') ? saved : 'dashboard';
  });

  const setActiveSection = (section) => {
    setActiveSectionState(section);
    try {
      localStorage.setItem('jobeazy_active_section', section);
    } catch {}
  };

  const [viewMode, setViewMode] = useState(() => (localStorage.getItem('jobeazy_jwt_token') ? 'app' : 'landing'));
  const [isLoginModalOpen, setIsLoginModalOpen] = useState(false);
  const [toastMessage, setToastMessage] = useState(null);
  const { theme, setTheme, toggleTheme } = useTheme();
  const [isCommandPaletteOpen, setIsCommandPaletteOpen] = useState(false);

  // Sync accountId with authenticated user or impersonated tenant
  useEffect(() => {
    if (impersonatedTenant?.id) {
      setAccountId(impersonatedTenant.id);
    } else if (user?.id) {
      setAccountId(user.id);
    }
  }, [user, impersonatedTenant]);

  // Ensure role-based section consistency
  useEffect(() => {
    if (user?.role === 'superadmin' && !impersonatedTenant && activeSection === 'dashboard') {
      setActiveSection('admin');
    } else if (user && user.role !== 'superadmin' && activeSection === 'admin') {
      setActiveSection('dashboard');
    }
  }, [user, impersonatedTenant]);

  // Data States
  const [jobs, setJobs] = useState([]);
  const [loadingJobs, setLoadingJobs] = useState(true);
  const [isIngesting, setIsIngesting] = useState(false);

  const [applications, setApplications] = useState([]);
  const [loadingApps, setLoadingApps] = useState(false);
  const [monitorSummary, setMonitorSummary] = useState({
    total: 0,
    draft: 0,
    sent: 0,
    follow_ups_due: 0,
    responded: 0,
    interview: 0,
    offer: 0,
    rejected: 0,
  });

  const [profile, setProfile] = useState(null);
  const [profileForm, setProfileForm] = useState({});
  const [isSavingProfile, setIsSavingProfile] = useState(false);

  const [stories, setStories] = useState([]);
  const [interviewTags, setInterviewTags] = useState([]);

  // Studio & Modal Selection States
  const [selectedJobForStudio, setSelectedJobForStudio] = useState(null);
  const [inspectingJob, setInspectingJob] = useState(null);

  const [tailorResult, setTailorResult] = useState(null);
  const [isTailoring, setIsTailoring] = useState(false);
  const [isSending, setIsSending] = useState(false);

  // Follow-Up & Materials Modals
  const [followUpModalApp, setFollowUpModalApp] = useState(null);
  const [followUpData, setFollowUpData] = useState(null);
  const [isSendingFollowUp, setIsSendingFollowUp] = useState(false);
  const [viewingMaterialsApp, setViewingMaterialsApp] = useState(null);

  const showToast = (msg, duration = 4000) => {
    setToastMessage(msg);
    setTimeout(() => setToastMessage(null), duration);
  };

  // Keyboard Shortcuts (Linear Ergonomics)
  useEffect(() => {
    const handleKeyDown = (e) => {
      if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'k') {
        e.preventDefault();
        setIsCommandPaletteOpen((prev) => !prev);
        return;
      }
      if (e.altKey && !e.ctrlKey && !e.metaKey) {
        if (e.key === '1') { e.preventDefault(); setActiveSection('dashboard'); }
        else if (e.key === '2') { e.preventDefault(); setActiveSection('jobs'); }
        else if (e.key === '3') { e.preventDefault(); setActiveSection('studio'); }
        else if (e.key === '4') { e.preventDefault(); setActiveSection('pipeline'); }
        else if (e.key === '5') { e.preventDefault(); setActiveSection('interview'); }
        else if (e.key === '6') { e.preventDefault(); setActiveSection('profile'); }
        else if (e.key === '7' && isSuperadmin) { e.preventDefault(); setActiveSection('admin'); }
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [isSuperadmin]);

  // Initial Data Loading - Only fetch candidate data for tenants or when superadmin is impersonating
  useEffect(() => {
    if (viewMode === 'app' && (!isSuperadmin || isImpersonating)) {
      fetchProfile();
      fetchJobs();
      fetchMonitorData();
      fetchInterviewData();
    }
  }, [accountId, viewMode, isSuperadmin, isImpersonating]);

  // Fetch Jobs
  const fetchJobs = async () => {
    try {
      setLoadingJobs(true);
      const res = await fetch(`${API_BASE}/jobs?account_id=${accountId}&include_gated=true&include_flagged=true&limit=100`, {
        headers: { ...authHeaders },
      });
      if (res.ok) {
        const data = await res.json();
        setJobs(Array.isArray(data) ? data : []);
      }
    } catch (err) {
      console.error('Failed to load jobs:', err);
    } finally {
      setLoadingJobs(false);
    }
  };

  // Fetch Monitor / Applications
  const fetchMonitorData = async () => {
    try {
      setLoadingApps(true);
      const [sumRes, appsRes] = await Promise.all([
        fetch(`${API_BASE}/applications/monitor/summary?account_id=${accountId}`, {
          headers: { ...authHeaders },
        }),
        fetch(`${API_BASE}/applications?account_id=${accountId}&limit=100`, {
          headers: { ...authHeaders },
        }),
      ]);
      if (sumRes.ok) {
        const sumData = await sumRes.json();
        setMonitorSummary(sumData);
      }
      if (appsRes.ok) {
        const appsData = await appsRes.json();
        setApplications(Array.isArray(appsData) ? appsData : []);
      }
    } catch (err) {
      console.error('Failed to load monitor data:', err);
    } finally {
      setLoadingApps(false);
    }
  };

  // Fetch Profile
  const fetchProfile = async () => {
    try {
      const res = await fetch(`${API_BASE}/profile?account_id=${accountId}`, {
        headers: { ...authHeaders },
      });
      if (res.ok) {
        const data = await res.json();
        setProfile(data);
        if (data) {
          setProfileForm({
            full_name: data.full_name || '',
            current_role: data.current_role || '',
            current_company: data.current_company || '',
            education: data.education || '',
            location_city: data.location_city || '',
            location_country: data.location_country || '',
            linkedin_url: data.linkedin_url || '',
            github_url: data.github_url || '',
            one_liner: data.one_liner || '',
            primary_identity: data.primary_identity || '',
            core_narrative: data.core_narrative || '',
            engineering_principle: data.engineering_principle || '',
            working_style: data.working_style || '',
            leadership_example: data.leadership_example || '',
            tone_preferences: data.tone_preferences || '',
            avoid_phrases: data.avoid_phrases || '',
            dealbreakers: data.dealbreakers || '',
          });
        }
      }
    } catch (err) {
      console.error('Failed to load profile:', err);
    }
  };

  // Fetch Interview Stories & Tags
  const fetchInterviewData = async () => {
    try {
      const [storiesRes, tagsRes] = await Promise.all([
        fetch(`${API_BASE}/interview/stories?account_id=${accountId}`, {
          headers: { ...authHeaders },
        }),
        fetch(`${API_BASE}/interview/tags?account_id=${accountId}`, {
          headers: { ...authHeaders },
        }),
      ]);
      if (storiesRes.ok) {
        const sData = await storiesRes.json();
        setStories(Array.isArray(sData) ? sData : []);
      }
      if (tagsRes.ok) {
        const tData = await tagsRes.json();
        setInterviewTags(Array.isArray(tData) ? tData : []);
      }
    } catch (err) {
      console.error('Failed to load interview data:', err);
    }
  };

  // Ingest Jobs Action
  const handleIngestJobs = async ({ query, location, source, limit }) => {
    try {
      setIsIngesting(true);
      const res = await fetch(`${API_BASE}/jobs/ingest`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          ...authHeaders,
        },
        body: JSON.stringify({
          account_id: accountId,
          query: query || 'AI Engineer',
          where: location || 'Remote',
          limit: limit || 10,
          source: source || undefined,
        }),
      });
      if (res.ok) {
        const data = await res.json();
        showToast(`Ingested ${data.new_jobs_count || 0} opportunities. ${data.flagged_count || 0} flagged by guard.`);
        fetchJobs();
      } else {
        showToast('Failed to ingest jobs from source feeds.', 4000);
      }
    } catch (err) {
      showToast('Error connecting to ingestion service.', 4000);
    } finally {
      setIsIngesting(false);
    }
  };

  // Save Profile
  const handleSaveProfile = async (e) => {
    e?.preventDefault();
    try {
      setIsSavingProfile(true);
      const res = await fetch(`${API_BASE}/profile?account_id=${accountId}`, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
          ...authHeaders,
        },
        body: JSON.stringify(profileForm),
      });
      if (res.ok) {
        showToast('Profile & Narrative grounding updated successfully!');
        fetchProfile();
      } else {
        showToast('Failed to save profile changes.', 4000);
      }
    } catch (err) {
      showToast('Error updating profile.', 4000);
    } finally {
      setIsSavingProfile(false);
    }
  };

  // Target Designation Handlers
  const handleAddDesignation = async (title, priority) => {
    try {
      const res = await fetch(`${API_BASE}/profile/designations?account_id=${accountId}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          ...authHeaders,
        },
        body: JSON.stringify({ title, priority, is_active: true }),
      });
      if (res.ok) {
        showToast(`Added target designation: "${title}"`);
        fetchProfile();
      }
    } catch (err) {
      showToast('Failed to add designation.', 4000);
    }
  };

  const handleDeleteDesignation = async (id) => {
    try {
      const res = await fetch(`${API_BASE}/profile/designations/${id}?account_id=${accountId}`, {
        method: 'DELETE',
        headers: { ...authHeaders },
      });
      if (res.ok) {
        showToast('Removed designation.');
        fetchProfile();
      }
    } catch (err) {
      showToast('Failed to remove designation.', 4000);
    }
  };

  // Target Location Handlers
  const handleAddLocation = async (location_name, location_type, relocation_willing) => {
    try {
      const res = await fetch(`${API_BASE}/profile/locations?account_id=${accountId}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          ...authHeaders,
        },
        body: JSON.stringify({ location_name, location_type, relocation_willing, is_active: true }),
      });
      if (res.ok) {
        showToast(`Added target location: "${location_name}"`);
        fetchProfile();
      }
    } catch (err) {
      showToast('Failed to add location.', 4000);
    }
  };

  const handleDeleteLocation = async (id) => {
    try {
      const res = await fetch(`${API_BASE}/profile/locations/${id}?account_id=${accountId}`, {
        method: 'DELETE',
        headers: { ...authHeaders },
      });
      if (res.ok) {
        showToast('Removed location.');
        fetchProfile();
      }
    } catch (err) {
      showToast('Failed to remove location.', 4000);
    }
  };

  // Compensation Handlers
  const handleSaveCompensation = async (compData) => {
    try {
      const res = await fetch(`${API_BASE}/profile/compensation?account_id=${accountId}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          ...authHeaders,
        },
        body: JSON.stringify(compData),
      });
      if (res.ok) {
        showToast('Compensation expectations updated.');
        fetchProfile();
      }
    } catch (err) {
      showToast('Failed to update compensation.', 4000);
    }
  };

  // Language Handlers
  const handleAddLanguage = async (language, proficiency) => {
    try {
      const res = await fetch(`${API_BASE}/profile/languages?account_id=${accountId}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          ...authHeaders,
        },
        body: JSON.stringify({ language, proficiency }),
      });
      if (res.ok) {
        showToast(`Added language: ${language}`);
        fetchProfile();
      }
    } catch (err) {
      showToast('Failed to add language.', 4000);
    }
  };

  const handleDeleteLanguage = async (id) => {
    try {
      const res = await fetch(`${API_BASE}/profile/languages/${id}?account_id=${accountId}`, {
        method: 'DELETE',
        headers: { ...authHeaders },
      });
      if (res.ok) {
        showToast('Removed language.');
        fetchProfile();
      }
    } catch (err) {
      showToast('Failed to remove language.', 4000);
    }
  };

  // Save Master CV LaTeX
  const handleSaveMasterCv = async (latexSource) => {
    try {
      const res = await fetch(`${API_BASE}/profile?account_id=${accountId}`, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
          ...authHeaders,
        },
        body: JSON.stringify({ master_cv_latex: latexSource }),
      });
      if (res.ok) {
        showToast('Master CV LaTeX template saved successfully.');
        fetchProfile();
      }
    } catch (err) {
      showToast('Failed to save master CV template.', 4000);
    }
  };

  // STAR Story Handlers
  const handleAddStory = async (storyPayload) => {
    try {
      const res = await fetch(`${API_BASE}/interview/stories?account_id=${accountId}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          ...authHeaders,
        },
        body: JSON.stringify(storyPayload),
      });
      if (res.ok) {
        showToast('Verified production STAR story added!');
        fetchInterviewData();
      }
    } catch (err) {
      showToast('Failed to create story.', 4000);
    }
  };

  const handleDeleteStory = async (id) => {
    try {
      const res = await fetch(`${API_BASE}/interview/stories/${id}?account_id=${accountId}`, {
        method: 'DELETE',
        headers: { ...authHeaders },
      });
      if (res.ok) {
        showToast('Story deleted.');
        fetchInterviewData();
      }
    } catch (err) {
      showToast('Failed to delete story.', 4000);
    }
  };

  // Studio: Tailor Application Action
  const handleTailorApplication = async ({ job_id, channel }) => {
    if (!job_id) {
      showToast('Please select a job from the radar.', 4000);
      return;
    }
    try {
      setIsTailoring(true);
      const res = await fetch(`${API_BASE}/applications/tailor`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          ...authHeaders,
        },
        body: JSON.stringify({
          account_id: accountId,
          job_id,
          channel: channel || 'email',
        }),
      });
      if (res.ok) {
        const data = await res.json();
        setTailorResult(data);
        showToast('LaTeX CV tailored & outreach drafted (Saved as Draft).');
        fetchMonitorData();
      } else {
        const err = await res.json();
        showToast(err.detail || 'Tailoring failed.', 5000);
      }
    } catch (err) {
      showToast('Error during CV tailoring.', 5000);
    } finally {
      setIsTailoring(false);
    }
  };

  // Strict Human Gate: Approve and Mark Sent
  const handleApproveAndSend = async ({ applicationId }) => {
    if (!applicationId) return;
    try {
      setIsSending(true);
      const res = await fetch(`${API_BASE}/applications/${applicationId}/send?account_id=${accountId}`, {
        method: 'POST',
        headers: { ...authHeaders },
      });
      if (res.ok) {
        showToast('Application approved & confirmed! 10-day follow-up scheduled.');
        fetchMonitorData();
        fetchJobs();
        setActiveSection('pipeline');
      } else {
        showToast('Failed to record send confirmation.', 4000);
      }
    } catch (err) {
      showToast('Error confirming send gate.', 4000);
    } finally {
      setIsSending(false);
    }
  };

  // Pipeline: Update Status
  const handleUpdateAppStatus = async (appId, newStatus) => {
    try {
      const res = await fetch(`${API_BASE}/applications/${appId}/status?account_id=${accountId}`, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
          ...authHeaders,
        },
        body: JSON.stringify({ status: newStatus }),
      });
      if (res.ok) {
        showToast(`Application moved to ${newStatus}`);
        fetchMonitorData();
      }
    } catch (err) {
      showToast('Failed to update status.', 4000);
    }
  };

  // Pipeline: Open Follow-Up Modal
  const handleDraftFollowUp = async (app) => {
    try {
      const res = await fetch(`${API_BASE}/applications/${app.id}/follow-up?account_id=${accountId}`, {
        method: 'POST',
        headers: { ...authHeaders },
      });
      if (res.ok) {
        const data = await res.json();
        setFollowUpData(data);
        setFollowUpModalApp(app);
      } else {
        setFollowUpData(null);
        setFollowUpModalApp(app);
      }
    } catch {
      setFollowUpData(null);
      setFollowUpModalApp(app);
    }
  };

  // Pipeline: Confirm Send Follow-Up
  const handleSendFollowUpConfirm = async (appId) => {
    try {
      setIsSendingFollowUp(true);
      const res = await fetch(`${API_BASE}/applications/${appId}/follow-up/send?account_id=${accountId}`, {
        method: 'POST',
        headers: { ...authHeaders },
      });
      if (res.ok) {
        showToast('Follow-up recorded! Next review scheduled.');
        setFollowUpModalApp(null);
        fetchMonitorData();
      } else {
        showToast('Failed to send follow-up.', 4000);
      }
    } catch (err) {
      showToast('Error sending follow-up.', 4000);
    } finally {
      setIsSendingFollowUp(false);
    }
  };

  // Navigate directly to Studio with a selected job
  const handleSelectJobForStudio = (job) => {
    setSelectedJobForStudio(job);
    setActiveSection('studio');
  };

  // Top recommended jobs
  const topJobs = useMemo(() => {
    return [...jobs].sort((a, b) => (b.match_score ?? 0) - (a.match_score ?? 0));
  }, [jobs]);

  // If user selected Landing Page view
  if (viewMode === 'landing') {
    return (
      <div className="landing-wrapper">
        <LandingPageView
          onOpenLogin={() => setIsLoginModalOpen(true)}
          onEnterApp={() => {
            if (token) {
              setViewMode('app');
            } else {
              setIsLoginModalOpen(true);
            }
          }}
          isAuthenticated={!!token}
          user={user}
        />
        <LoginModal
          isOpen={isLoginModalOpen}
          onClose={() => setIsLoginModalOpen(false)}
          onSuccess={(authData) => {
            setViewMode('app');
            if (authData?.role === 'superadmin') {
              setActiveSection('admin');
              showToast('Signed in as Superadmin. Switched to Superadmin Control Center.');
            } else {
              setActiveSection('dashboard');
              showToast(`Welcome back, ${authData?.email || 'Candidate'}!`);
            }
          }}
        />
        <Toast message={toastMessage} onClose={() => setToastMessage(null)} />
      </div>
    );
  }

  // If user role is NOT superadmin and they somehow landed on 'admin', redirect to 'dashboard'
  const effectiveSection = activeSection === 'admin' && !isSuperadmin ? 'dashboard' : activeSection;

  return (
    <div className="career-os-root">
      {/* SIDEBAR NAVIGATION (Candidate OS Workspace) */}
      <Sidebar
        activeSection={effectiveSection}
        setActiveSection={setActiveSection}
        profileName={
          impersonatedTenant
            ? (impersonatedTenant.name || impersonatedTenant.email)
            : (isSuperadmin
                ? 'SuperAdmin'
                : (profile?.full_name || user?.email?.split('@')[0] || 'Niloy Sannyal'))
        }
        tenantEmail={
          impersonatedTenant
            ? impersonatedTenant.email
            : (user?.email || (isSuperadmin ? 'admin@jobeazy.com' : 'niloy@example.com'))
        }
        isSuperadmin={isSuperadmin}
        showToast={showToast}
        theme={theme}
        setTheme={setTheme}
        toggleTheme={toggleTheme}
        onOpenCommandPalette={() => setIsCommandPaletteOpen(true)}
        onLogout={() => {
          logout();
          setViewMode('landing');
          showToast('Signed out of session.');
        }}
      />

      {/* MAIN CONTENT AREA */}
      <main className="career-os-main">
        {/* QA DOGFOODING IMPERSONATION BANNER */}
        {isImpersonating && impersonatedTenant && (
          <div className="impersonation-qa-banner">
            <div className="impersonation-banner-info">
              <span className="impersonation-tag">🧪 QA DOGFOOD MODE</span>
              <span className="impersonation-text">
                Testing workspace as tenant: <strong>{impersonatedTenant.name || impersonatedTenant.email}</strong>
                <span className="impersonation-subid"> (ID: {impersonatedTenant.id?.slice(0, 8)}...)</span>
              </span>
            </div>
            <button
              className="btn-exit-impersonation"
              onClick={() => {
                exitImpersonation();
                setActiveSection('admin');
                showToast('Exited QA mode. Returned to Superadmin Control Center.');
              }}
            >
              Exit to Admin Panel
            </button>
          </div>
        )}

        {/* SECTION 0: SUPERADMIN CONTROL (Accessible to superadmins only) */}
        {effectiveSection === 'admin' && isSuperadmin && (
          <AdminView
            currentSuperadminId={user?.id || accountId}
            onImpersonateTenant={(tenant) => {
              impersonateTenant(tenant);
              setActiveSection('dashboard');
              showToast(`Acting as tenant: ${tenant.email}`);
            }}
            showToast={showToast}
          />
        )}

        {/* SECTION 1: DASHBOARD */}
        {effectiveSection === 'dashboard' && (
          <DashboardView
            stats={{ total: jobs.length, high: jobs.filter((j) => (j.match_score ?? 0) >= 80).length }}
            monitorSummary={monitorSummary}
            profile={profile}
            topJobs={topJobs}
            onNavigate={setActiveSection}
            onSelectJobForStudio={handleSelectJobForStudio}
          />
        )}

        {/* SECTION 2: PROFILE & GROUNDING */}
        {effectiveSection === 'profile' && (
          <ProfileView
            profile={profile}
            profileForm={profileForm}
            setProfileForm={setProfileForm}
            onSaveProfile={handleSaveProfile}
            isSaving={isSavingProfile}
            targetDesignations={profile?.target_designations || []}
            onAddDesignation={handleAddDesignation}
            onDeleteDesignation={handleDeleteDesignation}
            targetLocations={profile?.target_locations || []}
            onAddLocation={handleAddLocation}
            onDeleteLocation={handleDeleteLocation}
            compensation={profile?.compensation || {}}
            onSaveCompensation={handleSaveCompensation}
            languages={profile?.spoken_languages || []}
            onAddLanguage={handleAddLanguage}
            onDeleteLanguage={handleDeleteLanguage}
            masterCvLatex={profile?.master_cv_latex || ''}
            onSaveMasterCv={handleSaveMasterCv}
            showToast={showToast}
          />
        )}

        {/* SECTION 3: JOBS & RADAR */}
        {effectiveSection === 'jobs' && (
          <JobsView
            jobs={jobs}
            loading={loadingJobs}
            onIngest={handleIngestJobs}
            isIngesting={isIngesting}
            onInspectJob={(job) => setInspectingJob(job)}
            onSelectJobForStudio={handleSelectJobForStudio}
            targetDesignations={profile?.target_designations || []}
          />
        )}

        {/* SECTION 4: APPLICATION STUDIO */}
        {effectiveSection === 'studio' && (
          <ApplicationStudio
            selectedJob={selectedJobForStudio}
            onSelectJob={setSelectedJobForStudio}
            jobs={jobs}
            applications={applications}
            profile={profile}
            onTailorApplication={handleTailorApplication}
            isTailoring={isTailoring}
            tailorResult={tailorResult}
            onApproveAndSend={handleApproveAndSend}
            isSending={isSending}
            showToast={showToast}
            onNavigate={setActiveSection}
          />
        )}

        {/* SECTION 5: PIPELINE KANBAN & TRACKER */}
        {effectiveSection === 'pipeline' && (
          <PipelineView
            applications={applications}
            loading={loadingApps}
            onUpdateStatus={handleUpdateAppStatus}
            onDraftFollowUp={handleDraftFollowUp}
            onSendFollowUp={handleSendFollowUpConfirm}
            onViewMaterials={(app) => setViewingMaterialsApp(app)}
            onNavigate={setActiveSection}
            showToast={showToast}
          />
        )}

        {/* SECTION 6: STAR INTERVIEW COACH */}
        {effectiveSection === 'interview' && (
          <InterviewCoachView
            stories={stories}
            tags={interviewTags}
            profile={profile}
            jobs={jobs}
            onAddStory={handleAddStory}
            onDeleteStory={handleDeleteStory}
            showToast={showToast}
          />
        )}
      </main>

      {/* MODALS */}
      {inspectingJob && (
        <JobDetailModal
          job={inspectingJob}
          onClose={() => setInspectingJob(null)}
          onApplyInStudio={handleSelectJobForStudio}
        />
      )}

      {followUpModalApp && (
        <FollowUpModal
          app={followUpModalApp}
          followUpData={followUpData}
          onClose={() => setFollowUpModalApp(null)}
          onSendFollowUp={handleSendFollowUpConfirm}
          isSending={isSendingFollowUp}
          showToast={showToast}
        />
      )}

      {viewingMaterialsApp && (
        <MaterialsModal
          app={viewingMaterialsApp}
          onClose={() => setViewingMaterialsApp(null)}
          showToast={showToast}
        />
      )}

      {/* GLOBAL COMMAND PALETTE (Ctrl+K / Cmd+K) */}
      <CommandPalette
        isOpen={isCommandPaletteOpen}
        onClose={() => setIsCommandPaletteOpen(false)}
        activeSection={effectiveSection}
        onNavigate={setActiveSection}
        theme={theme}
        setTheme={setTheme}
        jobs={jobs}
        onSelectJobForStudio={handleSelectJobForStudio}
        showToast={showToast}
      />

      <LoginModal
        isOpen={isLoginModalOpen}
        onClose={() => setIsLoginModalOpen(false)}
        onSuccess={(authData) => {
          setViewMode('app');
          if (authData?.role === 'superadmin') {
            setActiveSection('admin');
            showToast('Signed in as Superadmin. Switched to Superadmin Control Center.');
          } else {
            setActiveSection('dashboard');
            showToast(`Welcome back, ${authData?.email || 'Candidate'}!`);
          }
        }}
      />

      <Toast message={toastMessage} onClose={() => setToastMessage(null)} />
    </div>
  );
}

export default function App() {
  return (
    <AuthProvider>
      <CareerAppInner />
    </AuthProvider>
  );
}
