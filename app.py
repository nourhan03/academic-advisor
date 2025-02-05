import streamlit as st
import pandas as pd
from datetime import datetime

class ExpertSystem:
    def __init__(self, gpa, credits, major, attendance_rate=None, current_semester=None):
        self.knowledge_base = {
            'gpa': gpa,
            'credits': credits,
            'major': major,
            'attendance_rate': attendance_rate,
            'current_semester': current_semester,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.rules = []
        self.gpa = gpa
        self.credits = credits
        self.major = major

    def add_fact(self, key, value):
        """إضافة حقيقة إلى القاعدة المعرفية"""
        self.knowledge_base[key] = value

    def add_rule(self, condition, action):
        """إضافة قاعدة إنتاج"""
        self.rules.append((condition, action))

    def infer(self):
        """تطبيق محرك الاستدلال مع منع التكرار"""
        applied_rules = set()
        for condition, action in self.rules:
            if condition(self.knowledge_base) and action.__doc__ not in applied_rules:
                action(self.knowledge_base)
                applied_rules.add(action.__doc__)

    # القواعد الأكاديمية الأساسية
    def is_student_underperforming(self, kb):
        """التحقق إذا كان الطالب يعاني أكاديمياً"""
        return kb.get('gpa', 0) < 2.0

    def suggest_tutoring(self, kb):
        """اقتراح جلسات تقوية أكاديمية"""
        kb['academic_support'] = "يُنصح بحضور جلسات التقوية الأكاديمية وزيارة مركز دعم التعلم"
        kb['suggestion'] = "قم بحجز جلسات تقوية أكاديمية مع أساتذة المواد التي تواجه فيها صعوبة"

    def is_graduating_student(self, kb):
        """التحقق إذا كان الطالب يستعد للتخرج"""
        return kb.get('credits', 0) >= 120

    def suggest_graduation_clearance(self, kb):
        """اقتراح التحقق من إجراءات التخرج"""
        kb['graduation_status'] = "أنت مؤهل للتخرج"
        kb['graduation_requirements'] = [
            "التأكد من إكمال جميع المتطلبات الإجبارية",
            "مراجعة الخطة الدراسية مع المرشد الأكاديمي",
            "التحقق من إكمال متطلبات التدريب العملي",
            "تقديم طلب التخرج في البوابة الإلكترونية"
        ]
        kb['suggestion'] = "يرجى البدء في إجراءات التخرج والتواصل مع المرشد الأكاديمي"

    # قواعد تسجيل المقررات
    def suggest_course_registration(self, kb):
        """توصيات تسجيل المقررات"""
        major = kb.get('major', '')
        semester = kb.get('current_semester', 1)
        gpa = kb.get('gpa', 0)
        
        if gpa < 2.0:
            kb['registration_advice'] = "يُنصح بتسجيل الحد الأدنى من الساعات وإعادة المواد التي رسبت فيها"
            kb['max_hours'] = 12
        elif gpa >= 3.5:
            kb['registration_advice'] = "يمكنك تسجيل الحد الأقصى من الساعات المعتمدة"
            kb['max_hours'] = 21
        else:
            kb['registration_advice'] = "يمكنك تسجيل العبء الدراسي العادي"
            kb['max_hours'] = 18

        # إضافة توصيات خاصة بالتخصص
        if major in ['Physics', 'Mathematics']:
            kb['recommended_courses'] = "يُنصح بتسجيل مواد الرياضيات الأساسية أولاً"
        elif major in ['Chemistry', 'Biochemistry']:
            kb['recommended_courses'] = "يُنصح بتسجيل المعامل مع المحاضرات النظرية"
        elif major in ['Biology', 'Microbiology']:
            kb['recommended_courses'] = "يُنصح بالتركيز على المواد الأساسية في علوم الحياة"
        elif major in ['Computer Science', 'Statistics']:
            kb['recommended_courses'] = "يُنصح بتسجيل مواد البرمجة والإحصاء الأساسية أولاً"

    # قواعد تقييم الأداء
    def analyze_performance(self, kb):
        """تحليل أداء الطالب وتقديم تقييم عام"""
        gpa = kb.get('gpa', 0)
        attendance = kb.get('attendance_rate', 0)

        # تقييم المعدل
        if gpa >= 3.5:
            kb['performance'] = "ممتاز"
            kb['performance_details'] = "أداء متميز في جميع المواد"
        elif 2.5 <= gpa < 3.5:
            kb['performance'] = "جيد"
            kb['performance_details'] = "أداء جيد مع إمكانية التحسين"
        elif 2.0 <= gpa < 2.5:
            kb['performance'] = "مقبول"
            kb['performance_details'] = "بحاجة إلى تحسين الأداء الأكاديمي"
        else:
            kb['performance'] = "ضعيف"
            kb['performance_details'] = "بحاجة إلى اهتمام عاجل بالمستوى الأكاديمي"

        # تقييم الحضور
        if attendance is not None:
            if attendance < 75:
                kb['attendance_warning'] = "نسبة الحضور منخفضة وتحتاج إلى تحسين"
            else:
                kb['attendance_status'] = "نسبة الحضور جيدة"

    # قواعد تتبع الحضور
    def analyze_attendance(self, kb):
        """تحليل نسبة الحضور وتقديم التوصيات"""
        attendance = kb.get('attendance_rate', 0)
        if attendance < 75:
            kb['attendance_status'] = "منخفض"
            kb['attendance_advice'] = "يجب تحسين نسبة الحضور لتجنب الحرمان"
        elif 75 <= attendance < 85:
            kb['attendance_status'] = "مقبول"
            kb['attendance_advice'] = "نسبة الحضور مقبولة ولكن تحتاج إلى تحسين"
        else:
            kb['attendance_status'] = "جيد"
            kb['attendance_advice'] = "استمر في المحافظة على نسبة الحضور الجيدة"

    # قواعد توصيات المسارات الأكاديمية
    def suggest_academic_path(self, kb):
        """تقديم توصيات حول المسار الأكاديمي"""
        major = kb.get('major', '')
        gpa = kb.get('gpa', 0)
        credits = kb.get('credits', 0)

        # توصيات عامة حسب المستوى الدراسي
        if credits < 30:
            kb['academic_level'] = "سنة أولى"
            kb['path_advice'] = "ركز على المواد الأساسية وتطوير مهارات الدراسة"
        elif 30 <= credits < 60:
            kb['academic_level'] = "سنة ثانية"
            kb['path_advice'] = "ابدأ في استكشاف التخصصات الدقيقة والفرص البحثية"
        elif 60 <= credits < 90:
            kb['academic_level'] = "سنة ثالثة"
            kb['path_advice'] = "ابحث عن فرص التدريب والمشاريع البحثية"
        else:
            kb['academic_level'] = "سنة رابعة"
            kb['path_advice'] = "ركز على مشروع التخرج والتحضير للدراسات العليا أو سوق العمل"

        # توصيات خاصة بالتخصص
        if major in ['Physics', 'Mathematics']:
            kb['specialization_advice'] = "فكر في التخصص في مجالات مثل الفيزياء النظرية، الفلك، أو الرياضيات التطبيقية"
        elif major in ['Chemistry', 'Biochemistry']:
            kb['specialization_advice'] = "استكشف مجالات الكيمياء العضوية، التحليلية، أو الحيوية"
        elif major in ['Biology', 'Microbiology']:
            kb['specialization_advice'] = "فكر في التخصص في علم الأحياء الجزيئي، علم الأحياء الدقيقة، أو التقنية الحيوية"
        elif major in ['Computer Science', 'Statistics']:
            kb['specialization_advice'] = "استكشف مجالات علوم البيانات، الذكاء الاصطناعي، أو تطوير البرمجيات"

def create_expert_system_app():
    st.title("نظام الإرشاد الأكاديمي - كلية العلوم")
    st.write("أدخل معلومات الطالب للحصول على النصائح والتوصيات")

    with st.form("student_info"):
        col1, col2 = st.columns(2)
        
        with col1:
            gpa = st.number_input("المعدل التراكمي", min_value=0.0, max_value=4.0, value=2.0, step=0.1)
            credits = st.number_input("الساعات المكتسبة", min_value=0, max_value=150, value=60)
            attendance_rate = st.number_input("نسبة الحضور (%)", min_value=0, max_value=100, value=80)

        with col2:
            major = st.selectbox("التخصص", [
                "Physics",
                "Mathematics",
                "Chemistry",
                "Biochemistry",
                "Biology",
                "Microbiology",
                "Computer Science",
                "Statistics",
                "Geology"
            ])
            current_semester = st.selectbox("المستوى الدراسي", [
                "المستوى الأول",
                "المستوى الثاني",
                "المستوى الثالث",
                "المستوى الرابع",
                "المستوى الخامس",
                "المستوى السادس",
                "المستوى السابع",
                "المستوى الثامن"
            ])
            registration_open = st.checkbox("فترة التسجيل مفتوحة")

        submit_button = st.form_submit_button("تحليل الحالة الأكاديمية")

    if submit_button:
        try:
            system = ExpertSystem(
                gpa=gpa,
                credits=credits,
                major=major,
                attendance_rate=attendance_rate,
                current_semester=current_semester
            )
            system.add_fact('registration_open', registration_open)

            # إضافة جميع القواعد
            system.add_rule(system.is_student_underperforming, system.suggest_tutoring)
            system.add_rule(system.is_graduating_student, system.suggest_graduation_clearance)
            system.add_rule(lambda kb: True, system.analyze_performance)
            system.add_rule(lambda kb: True, system.analyze_attendance)
            system.add_rule(lambda kb: True, system.suggest_course_registration)
            system.add_rule(lambda kb: True, system.suggest_academic_path)

            # تنفيذ الاستدلال
            system.infer()

            # عرض النتائج في تبويبات
            tab1, tab2, tab3, tab4, tab5 = st.tabs([
                "الحالة الأكاديمية",
                "تسجيل المقررات",
                "تقييم الأداء",
                "متابعة الحضور",
                "التوصيات والمسارات"
            ])

            with tab1:
                st.subheader("الحالة الأكاديمية العامة")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("المعدل التراكمي", f"{gpa:.2f}")
                with col2:
                    st.metric("الساعات المكتسبة", credits)
                with col3:
                    remaining_credits = 120 - credits
                    st.metric("الساعات المتبقية للتخرج", max(0, remaining_credits))
                
                if 'academic_level' in system.knowledge_base:
                    st.info(f"المستوى الدراسي: {system.knowledge_base['academic_level']}")
                if 'academic_support' in system.knowledge_base:
                    st.warning(system.knowledge_base['academic_support'])
                if 'graduation_status' in system.knowledge_base:
                    st.success(system.knowledge_base['graduation_status'])
                    if 'graduation_requirements' in system.knowledge_base:
                        st.write("متطلبات التخرج:")
                        for req in system.knowledge_base['graduation_requirements']:
                            st.write(f"- {req}")

            with tab2:
                st.subheader("توصيات تسجيل المقررات")
                if 'registration_advice' in system.knowledge_base:
                    st.info(system.knowledge_base['registration_advice'])
                if 'max_hours' in system.knowledge_base:
                    st.metric("الحد الأقصى للساعات المسموح بها", system.knowledge_base['max_hours'])
                if 'recommended_courses' in system.knowledge_base:
                    st.success(system.knowledge_base['recommended_courses'])

            with tab3:
                st.subheader("تقييم الأداء")
                if 'performance' in system.knowledge_base:
                    performance = system.knowledge_base['performance']
                    performance_color = {
                        "ممتاز": "🟢",
                        "جيد": "🟡",
                        "مقبول": "🟠",
                        "ضعيف": "🔴"
                    }
                    st.markdown(f"### مستوى الأداء: {performance_color.get(performance, '')} {performance}")
                    
                if 'performance_details' in system.knowledge_base:
                    st.info(system.knowledge_base['performance_details'])

            with tab4:
                st.subheader("متابعة الحضور")
                st.metric("نسبة الحضور", f"{attendance_rate}%")
                if 'attendance_status' in system.knowledge_base:
                    status_color = {
                        "جيد": "🟢",
                        "مقبول": "🟡",
                        "منخفض": "🔴"
                    }
                    st.markdown(f"### حالة الحضور: {status_color.get(system.knowledge_base['attendance_status'], '')} {system.knowledge_base['attendance_status']}")
                
                if 'attendance_advice' in system.knowledge_base:
                    st.info(system.knowledge_base['attendance_advice'])
                if 'attendance_warning' in system.knowledge_base:
                    st.warning(system.knowledge_base['attendance_warning'])

            with tab5:
                st.subheader("التوصيات والمسارات الأكاديمية")
                if 'path_advice' in system.knowledge_base:
                    st.info(system.knowledge_base['path_advice'])
                if 'specialization_advice' in system.knowledge_base:
                    st.success(system.knowledge_base['specialization_advice'])

                # عرض تفاصيل إضافية في صندوق قابل للتوسيع
                with st.expander("عرض جميع التفاصيل"):
                    st.json(system.knowledge_base)

        except Exception as e:
            st.error(f"حدث خطأ: {str(e)}")

if __name__ == "__main__":
    st.set_page_config(
        page_title="نظام الإرشاد الأكاديمي - كلية العلوم",
        page_icon="🎓",
        layout="wide"
    )
    create_expert_system_app()
