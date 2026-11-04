import { jsPDF } from 'jspdf';
import { compileParsedLatexToPdf } from '../../utils/latexCompiler';

export const sanitizeFileName = (name) => {
  return (name || 'Application')
    .replace(/&amp;/g, 'and')
    .replace(/&lt;/g, '')
    .replace(/&gt;/g, '')
    .replace(/&#39;/g, '')
    .replace(/&quot;/g, '')
    .replace(/&/g, 'and')
    .replace(/[^\w\s-]/g, '')
    .replace(/[-\s]+/g, '_')
    .replace(/_+/g, '_')
    .trim();
};

export const downloadLatexSource = (editedLatex, profile, customCompany, showToast) => {
  const content = editedLatex || profile?.master_cv_latex || '';
  const blob = new Blob([content], { type: 'text/x-tex;charset=utf-8' });
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  const comp = sanitizeFileName(customCompany || 'Application');
  link.download = `Tailored_CV_${comp}.tex`;
  link.click();
  URL.revokeObjectURL(url);
  showToast('Downloaded tailored LaTeX CV');
};

export const downloadPdfDocument = ({
  activeDraftTab,
  parsedDoc,
  customCompany,
  customRole,
  profile,
  editedCoverDraft,
  editedOutreachDraft,
  showToast,
}) => {
  try {
    const comp = sanitizeFileName(customCompany || 'Application');
    const role = customRole || 'AI Engineer';
    const candidateName = profile?.full_name || 'Niloy Sannyal';

    if (activeDraftTab === 'latex') {
      const doc = compileParsedLatexToPdf(parsedDoc, `Tailored_CV_${comp}.pdf`);
      doc.save(`Tailored_CV_${comp}.pdf`);
      showToast(`Downloaded Tailored_CV_${comp}.pdf!`);
    } else {
      const doc = new jsPDF({
        orientation: 'portrait',
        unit: 'pt',
        format: 'a4',
      });

      doc.setFont('helvetica', 'bold');
      doc.setFontSize(18);
      doc.setTextColor(17, 24, 39);
      doc.text(candidateName, 40, 50);

      doc.setFont('helvetica', 'normal');
      doc.setFontSize(9.5);
      doc.setTextColor(75, 85, 99);
      doc.text('Dhaka, Bangladesh | niloysannyal@gmail.com | +8801783445245 | niloysannyal.me', 40, 68);

      doc.setDrawColor(209, 213, 219);
      doc.setLineWidth(1);
      doc.line(40, 78, 555, 78);

      let y = 105;
      doc.setFontSize(10);
      doc.setTextColor(55, 65, 81);
      doc.text(
        `Date: ${new Date().toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' })}`,
        40,
        y
      );

      y += 16;
      doc.setFont('helvetica', 'bold');
      doc.text(`To: Hiring Team at ${comp}`, 40, y);
      y += 14;
      doc.text(`Regarding: Application for ${role}`, 40, y);

      y += 24;
      doc.setFont('helvetica', 'normal');
      doc.setFontSize(10);

      const textToSplit = activeDraftTab === 'cover' ? editedCoverDraft : editedOutreachDraft;
      const paragraphs = (textToSplit || '').split(/\n\s*\n/);

      paragraphs.forEach((p) => {
        const splitP = doc.splitTextToSize(p.trim(), 515);
        doc.text(splitP, 40, y);
        y += splitP.length * 14 + 10;
      });

      doc.save(`Cover_Letter_${comp.replace(/\s+/g, '_')}.pdf`);
      showToast(`Downloaded Cover_Letter_${comp}.pdf!`);
    }
  } catch (err) {
    console.error('PDF generation error:', err);
    showToast('Error generating PDF document.', 4000);
  }
};

