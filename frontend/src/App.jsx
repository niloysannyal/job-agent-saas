import React, { useState, useEffect, useMemo } from 'react';
import './App.css';

import Sidebar from './components/Sidebar';
import DashboardView from './components/DashboardView';
import ProfileView from './components/ProfileView';
import JobsView from './components/JobsView';
import ApplicationStudio from './components/ApplicationStudio';
import PipelineView from './components/PipelineView';
import InterviewCoachView from './components/InterviewCoachView';
import JobDetailModal from './components/JobDetailModal';
import FollowUpModal from './components/FollowUpModal';
import MaterialsModal from './components/MaterialsModal';
import Toast from './components/Toast';

// Default Tenant: Niloy Sannyal (seeded in database)
const DEFAULT_ACCOUNT_ID = '6e488188-0015-4657-94c9-92d01413dcfb';
const API_BASE = '/api/v1';

export default function App() {
  const [accountId, setAccountId] = useState(DEFAULT_ACCOUNT_ID);
  const [activeSection, setActiveSection] = useState('dashboard'); // dashboard | profile | jobs | studio | pipeline | interview
  const [toastMessage, setToastMessage] = useState(null);

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

  // --- Initial Data Loading ---
  useEffect(() => {
    fetchProfile();
    fetchJobs();
    fetchMonitorData();
    fetchInterviewData();
  }, [accountId]);

  // Fetch Jobs
  const fetchJobs = async () => {
    try {
      setLoadingJobs(true);
      const res = await fetch(`${API_BASE}/jobs?account_id=${accountId}&include_gated=true&include_flagged=true&limit=100`);
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
        fetch(`${API_BASE}/applications/monitor/summary?account_id=${accountId}`),
        fetch(`${API_BASE}/applications?account_id=${accountId}&limit=100`),
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
      const res = await fetch(`${API_BASE}/profile?account_id=${accountId}`);
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
        fetch(`${API_BASE}/interview/stories?account_id=${accountId}`),
        fetch(`${API_BASE}/interview/tags?account_id=${accountId}`),
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
        headers: { 'Content-Type': 'application/json' },
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
        headers: { 'Content-Type': 'application/json' },
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
        headers: { 'Content-Type': 'application/json' },
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
        headers: { 'Content-Type': 'application/json' },
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
        headers: { 'Content-Type': 'application/json' },
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
        headers: { 'Content-Type': 'application/json' },
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
        headers: { 'Content-Type': 'application/json' },
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
        headers: { 'Content-Type': 'application/json' },
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
        headers: { 'Content-Type': 'application/json' },
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
        headers: { 'Content-Type': 'application/json' },
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
  const handleSendFollowUpConfirm = async (appId, draftText) => {
    try {
      setIsSendingFollowUp(true);
      const res = await fetch(`${API_BASE}/applications/${appId}/follow-up/send?account_id=${accountId}`, {
        method: 'POST',
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

  // Global counts for Sidebar badges
  const sidebarCounts = useMemo(() => {
    const highMatch = jobs.filter((j) => (j.match_score ?? 0) >= 80).length;
    return {
      jobs: jobs.length,
      highMatch,
      designations: profile?.target_designations?.length || 0,
      tailoredDrafts: monitorSummary.draft || 0,
      pipeline: monitorSummary.total || 0,
      followUpsDue: monitorSummary.follow_ups_due || 0,
      stories: stories.length,
    };
  }, [jobs, profile, monitorSummary, stories]);

  const topJobs = useMemo(() => {
    return [...jobs].sort((a, b) => (b.match_score ?? 0) - (a.match_score ?? 0));
  }, [jobs]);

  return (
    <div className="career-os-root">
      {/* SIDEBAR NAVIGATION */}
      <Sidebar
        activeSection={activeSection}
        setActiveSection={setActiveSection}
        profileName={profile?.full_name || 'Niloy Sannyal'}
        tenantEmail={profile?.email || 'niloy@example.com'}
        showToast={showToast}
      />

      {/* MAIN CONTENT AREA */}
      <main className="career-os-main">
        {/* SECTION 1: DASHBOARD */}
        {activeSection === 'dashboard' && (
          <DashboardView
            stats={{ total: jobs.length, high: sidebarCounts.highMatch }}
            monitorSummary={monitorSummary}
            profile={profile}
            topJobs={topJobs}
            onNavigate={setActiveSection}
            onSelectJobForStudio={handleSelectJobForStudio}
          />
        )}

        {/* SECTION 2: PROFILE & GROUNDING */}
        {activeSection === 'profile' && (
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
        {activeSection === 'jobs' && (
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
        {activeSection === 'studio' && (
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
        {activeSection === 'pipeline' && (
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
        {activeSection === 'interview' && (
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

      <Toast message={toastMessage} onClose={() => setToastMessage(null)} />
    </div>
  );
}
