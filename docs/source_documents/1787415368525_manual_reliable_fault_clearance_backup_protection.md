# Manual on Reliable Fault Clearance and Back-up Protection of EHV and UHV Transmission Networks

*Publication No. 296*  
*Central Board of Irrigation and Power, New Delhi — September 2005*  
*ISBN 81-7336-303-X*

*Editors: G.N. Mathur, B.S. Palki, Kuldip Singh*

---

*Note: This markdown was generated via OCR text extraction from a scanned PDF (Adobe Acrobat Paper Capture). Minor OCR artifacts may remain in places, especially in tables and figures, which don't extract well as text. Advertisement pages bound into the original manual (front/back matter) have been omitted; the technical content and chapter structure follow the original document.*

---

## Table of Contents

- [Chapter 1: Introduction](#chapter-1-introduction)
- [Chapter 2: Fundamentals](#chapter-2-fundamentals)
- [Chapter 3: Requirements](#chapter-3-requirements)
- [Chapter 4: Performance Indices](#chapter-4-performance-indices)
- [Chapter 5: Lines and Cables](#chapter-5-lines-and-cables)
- [Chapter 6: Power Transformers](#chapter-6-power-transformers)
- [Chapter 7: Shunt Reactors](#chapter-7-shunt-reactors)
- [Chapter 8: Busbars](#chapter-8-busbars)
- [Chapter 9: DC Auxiliary Supply Systems](#chapter-9-dc-auxiliary-supply-systems)
- [Chapter 10: Switching Devices](#chapter-10-switching-devices)
- [Chapter 11: Communication Systems](#chapter-11-communication-systems)
- [Chapter 12: References](#chapter-12-references)

## Foreword

FOREWORD
        Reliable clearance of a fault, when it occurs in the
power system network, is critical for maintaining power
system stability, for avoiding system collapse and for better
grid operation. This manual as the name suggests deals with
the subject of reliable fault clearance and ways of providing
main and back-up protection to various power system
elements in EHV and UHV transmission networks.
         We must not assume that all elements in the fault clearance system
always operate correctly. Protection relays may fail to operate or may operate
when they should not. Switching devices may fail to interrupt the fault current.
It is a common practice in EHVand UHV networks to duplicate the protection
systems. In addition back-up protection is provided to operate when a power
system fault is not cleared, or abnormal condition is not detected, in the
required time because of failure or inability of the main protections to operate
or failure of the appropriate circuit breaker(s) to trip.
         By providing back-up protection, it is possible to reduce the risk of
wide spread disturbances when a protection relay or a switching device fails
to operate. The main protection and the back-up protection may reside in
different substations (remote back-up) or in the same substation (local back-
up). In case of local back-up, it can be a substation local back-up and/or
circuit local back-up protection.
       The requirements of the back-up protection cannot be independent of
the requirements of the entire fault clearance system. Back-up protection is
an important function of the protection system and its design needs to be
coordinated with the design of the main protection. Therefore the protection
engineer should work in close cooperation with system planners and designers.
        Even though back-up protection is the focus of this manual, any
discussions concerning it cannot be separated from main protection. Thus
the manual deals with issues involved in complete protection system viz.,
main protection, duplicate protection and back-up protection for various power
system elements in a comprehensive way. The elements covered are Lines!
Cables, Power transformers, Shunt reactors, Bus bars and Breaker fail
protection.
     The manual also reviews briefly current practices and makes
recommendations for selection and application of various main and back-up
                                      (v)

protections. A careful study of the manual will help understand the reasons
behind many of the practices currently followed and help utilities fine-tune
them. I also notice that in a number of places reference has been made to
another CBIP manual (No. 274) titled "Protection of Generators, Generator
Transformers and 220 kV and 400 kV Networks". The two manuals
complement each other.
        I am sure that the present publication will prove to be a very useful
guide for the Power Utilities, Manufacturers, and concerned engineers,
particularly to those who have so far been deprived of a unified document on
the subject, and it gives them an insight to a number of aspects that should
help them in managing the reliability and availability of protection system
better.
        I appreciate the efforts made by Central Board of Irrigation and Power
in bringing out this document and congratulate them for their initiative. I also
appreciate the efforts made by Working Group in bringing out this
comprehensive document and commend the invaluable contribution of the
members in bringing out this manual.
With Best Wishes

September 2005                                               Bhanu Bhushan
New Delhi                                                    Member, CERC

                                      (vi)

## Preface

PREFACE
      With Indian economy growing and expectations of
industries and consumers using electricity increasing,
providing reliable power supply is becoming increasingly
important. To meet this challenge new power stations are
being added and T&D networks are continuously being
strengthened. Formation of national grid is one major step in
this direction.
     Protection and Automation system provided in the power system has
an important role to play in meeting the challenge of providing reliable power
supply. Within this, the protection system for various power system elements
plays a major role. Two of the important requirements on protection system
are dependability and security to provide reliable fault clearance.
     To increase the reliability of fault clearance system in the event of failure
of main protection or circuit breaker, duplicate main protection and back-up
protections are provided. Even though protection practices to be followed in
case of EHV and UHV networks are well established and documented, yet
a need for separate document on the subject of back-up protection to serve
as guide to utilities in India has long been felt.
        In October 2001, CBIP organized 2nd International Conference on
"Integrated Protection, Control and Communication, Experience, Benefits and
Trends". During the valedictory session of this conference, it was decided
that CBIP should constitute a working group to come out with a report on
BACK-UP PROTECTION to serve as a guide to utilities in India. Accordingly,
CBIP constituted a Working Group under the chairmanship of Shri B.S. Palki,
Regular Member CIGRE Study Committee B5 (Protection & Automation)
from ABB Limited, Bangalore and experts in the field drawn from various
utilities, manufacturers and academic institutions in India.
     The Working Group, as a result of their untiring and sincere efforts of
more than three years, has come out with a comprehensive document titled,
"Manual on Reliable fault clearance and back-up protection of EHV and UHV
transmission networks". Over the period of last three years there were
seven formal meetings of the group, each lasting for two days and several
informal meetings and discussions to arrive at the structure of the manual
and finalise its contents.

                                       (vii)

     The manual gives basic concepts of back-up protection, requirements
placed on the protection system from the power system and includes
discussions on main and back-up protection systems for Lines! Cables,
Power transformers, Shunt reactors, Bus bars and Breaker fail protection.
Discussions on DC system and communication system, which form important
elements of the protection system, are also included. Use of performance
indices to assess dependability and security of protection system to serve
as tool to make continuous improvements is a new concept for our utilities
and this is covered in a separate chapter. In each chapter suggestions and
recommendations have been made for the guidance of the utilities to review
the current practices and make changes and adopt wherever necessary.
       The quantum of technical work involved in completion of this manual
could not have been accomplished without the untiring efforts and invaluable
contribution of the members of the Expert Group & CBIP. The Central Board
of Irrigation and Power thankfully acknowledges contribution of all the members
of the Working Group drawn from various utilities, academic institutions and
manufacturers for their valuable contributions. Special thanks are due
to Shri B.S. Palki, Chairman of the Expert Group for the tremendous input
and direction given in finalizing the manual. He also formulated the draft of
this manual and then incorporated the suggestions/feedback received from
the various members. The contribution of Shri Mata Prasad, Shri Vikas
Saksena from POWERGRID, Shri S.G. Patki from Tata Power, Shri SK Ray
Mohapatra from Central Electricity Authority and Shri Pramed Kumar from NTPC
for their active involvement in giving final shape to the manual needs prominent
mention.
        It is hoped that this manual will help the protection engineers of various
utilities in India in managing the availability and reliability of the fault clearance
system in transmission networks in the voltage range from 132 kV to 765 kV.

                                                                        G.N. Mathur
September 2005                                                             Secretary
New Delhi                                  Central Board of Irrigation and Power

## Chapter 1: Introduction

INTRODUCTION
The Indian power system is growing steadily. To match with the growing demand,
transmission system is also expanding with 765 kV AC lines overlaid on existing
400 kV system, new long distance HVDC links in hybrid mode and providing series
compensation including TCSC wherever feasible on existing 400 kV and 220 kV
lines etc. With the development of regional grids and interregional ties to form
ultimately national and intemational grids, the power system is becoming more and
more complex.

      Along with this growth, requirement of high availability and reliable operation
of large generating plants with EHV and UHV transmission network assume
tremendous importance in maintaining power system stability for better grid
operation. To realize the vision of "Reliable, Affordable and Quality Power for All"
some changes will be required in our approach towards integrated protection and
automation system planning.

       The protection and automation system used in the network plays an important
role in meeting this requirement, preventing system collapse during major system
disturbances, reducing outage time and minimizing the possibility of damage to the
machines and equipment. Utilities should install protection systems that are
dependable. Here, dependability is the probability of not failing to clear a power
system fault or abnormality.

     The manual deals predominantly with this subject viz.: how to enhance
dependability of fault clearance system.

       When a fault occurs in the network a protective relay may fail to operate or a
circuit breaker may fail to open and interrupt the fault current. Such failures of a
protective relay or a switching device may prevent proper clearance of the faull.

      The addition of a second main protection increases the availability and
dependability of fault clearance system. In addition, the provision of back-up
protection that operates independently of specified devices in the main protection
system enhances this further. It can be generally said that provision of second main
protection and back-up protections enhances the dependability of the fault clearance
system.

      While the provision of second main protection and back-up protection
enhances the dependability of fault clearance system it increases the costs.
Therefore there is often a tendency to choose to run the power system without a
reserve protection and adequate back-up protection in the network. At voltage levels
of 220 kV and below this is often the case.

2                 Manual on Reliable FauN elBa"""", and Back-Up _   of
                             EHVand UHV Tnmsmission N9Iwot1rs

       Since the number of shunt faults is high, consequences of failure to clear a
fault may be serious and results in high disturbance costs that are far greater than
the costs involved in providing additional protections.

      The disturbance costs include the following:

•     Costs associated with the risk of injury to people and damage to third party
      property
•     Costs associated with the risk of damage to power lines and other power
      apparatus
•     Costs associated with the customer outages
•     Costs associated with the voltage disturbances
•     Costs associated with the customers' complaints and ill will.
      Therefore the utilities should base the decisions for provision of additional
protection and back-up protection considering the costs involved in terms of
disturbances leading towards uncleared faults. Recommendations made in this
manual have been done considering the above. It is further suggested that the
protection engineer should keep this aspect in mind while reviewing protection
system in any given case.
      The manual is structured as under.
•     Chapter 2 defines some fundamental concepts of back-up protection.
•     Chapter 3 describes briefly the external requirements for protective systems
      that could come in future from external authorities, governmental and other
      agencies, equipment manufacturers, insurance companies, standardization
      organizations, utilities and customers.
•     Chapter 4 defines some performance indices for protection devices and
      switching devices.
•     Chapter 5 to 8 deals with the different power system components such as:
      transmission circuits (overhead lines and underground cables) power
      transformers, bus bars and shunt reactors. Each chapter contains,
      requirements on the protection system, practices of protection and a final
      section on back-up protection.
•     Chapter 9 deals with the DC auxiliary supply system and redundancy in the
      DC supply system.
•     Chapter 10 deals with the performance of switching devices and circuit-
      breaker failure protection.
•     Chapter 11 deals with reliability and redundancy of telecommunication
      systems.
•     Chapter 12 gives some references.

                                 Chapter 1 : Introduction                              3

      While preparing the manual the working group has used a report on this
subject prepared by CIGRE working group SC 34; WG:01 titled "Reliable fault
clearance and back-up protection". It has been a valuable source of information to
the working group entrusted with preparation of this manual.

      Another document referred while preparing this is CBIP manual (No 274) titled
"Protection of Generators, Generator Transformers and 220 kV and 400 kV
Networks". Reference has been made to this particularly while making
recommendations to utilities in India.

      In conclusion it can be said that even though back-up protection is the focus of
this manual, any discussion concerning it cannot be separated from the Main
protection and thus the manual deals with issues involved for complete protection
system including Main and Back-up protection. Appropriate recommendations have
been made in various places, where it is felt that they are departures from the
current practices.

        Finally it is hoped that the manual will help the protection engineers of various
utilities in India in managing the availability and reliability of the fault clearance
system in transmission networks in the voltage range from 132 kV to
765 kV.

## Chapter 2: Fundamentals

FUNDAMENTALS
A back-up protection is intended to operate when a power system fault is not
cleared, or an abnormal condition is not detected, in the required time because of
failure or inability of main protections to operate or failure of the appropriate circuit-
breaker(s) to trip. The back-up protection, by definition, is slower than main
protection. Back-up protection is installed to improve the dependability of the fault
clearance system. Here, dependability is the probability of not failing to clear a
power system fault or abnormality.

      Back-up protection shall operate when main protection fails to clear a fault. In
such a case, the protection may not operate correctly, the circuit breaker may not
receive any tripping command or the circuit breaker may fail to open and interrupt
the fault current. Such failures of a protective relay or a switching device may
prevent proper clearance of the fault.

      Sometimes a second main protection or duplicate protection, intended to
operate if the main protection system fails to operate or is temporarily out of service
is provided. This, however, should not be mixed up with back-up protection. The
second main protection is there to increase the dependability of normal fault clearing
mechanism and it must always operate very selectively, while the back-up protection
may operate with less selectivity because it operates after some time delay.

      The requirements on back-up protection cannot be independent of the
requirements on the entire fault clearance system.

      Use of elementary form of the single-failure criterion is often done while
planning protection system arrangement. It requires that the failure of anyone
component in a fault clearance system should not result in a complete failure to
clear a power system fault or abnormality.

      Back-up protection is an important function of the protection system, and its
design needs to be coordinated with the design of the main protection. In this
process, it is suggested that the protection engineer should work closely with the
power system planners and designers.

      The system planner should inform the protection engineer regarding
assumptions made during system design and requirements on fault clearance
system at various voltage levels in the system. He must inform him of the needs of
the protection system that must fulfill, as for example, the total fault clearance time.
The protection engineer must also be familiar with the following:
•     System requirements

6                 Manual on RsliabIB Faun C/sarancs and Back-Up Protection of
                             EHVand UHV Transmission Networlrs

•     The system design criteria
•     The plant specifications
•     The failure rates of the protected plant
•     The requirements of performance indices of the fault clearance system
•     The requirements of reliability of protection equipment
•     The probability that a switching device fails to interrupt the fault current.

       The power system planner should help the protection engineer in formulating
the requirements of the fault clearance system. Points to be considered are the
stability of the power system and the type of bus bar arrangement and switching
scheme. Protection engineers and the power system designers must co-ordinate the
demands on fault clearance system, as also the performance of station equipment
and strike a balance between technical and economical benefits and the risks
associated with making the protection system more complex.

2.1   FAULT CLEARANCE SYSTEMS
The basic task of any fault clearance system is to detect a specified class of power
system faults and abnormalities and to disconnect the associated item of substation
or plant from the rest of the power system. Figure 2.1 shows the components of a
fault clearance system. Here TE stands for teleprotection equipment.

      The faulty component should be disconnected as fast as possible and with
minimum disturbance to the consumers and minimum damage to the power
apparatus. An essential property of the fault clearance system is reliability. Reliability
of protection includes dependability and security of protection. Fault analysis and
relay co-ordination are important issues for the reliability of protection systems.

      A power system fault is a power system abnormality that involves, or is the
result of, failure of primary equipment and normally requires the immediate
disconnection of the faulty equipment from the rest of the power system by tripping
of the appropriate circuit breakers. Power system faults can be shunt, series or
combination faults.

      A non-power system fault tripping is an unwanted tripping of a circuit breaker
as a result of faults, other than the power system faults. The unwanted operations of
a protection in the absence of a power system fault or the tripping of a breaker due
to other secondary equipment failure or due to human error are examples of non-
power system fault.

                                   Chapter 2 : Fundamentals                             7

                                                                            /'

                   Protection System

              CT    r-                                    Circuit Breaker

              VT    r-     Protection
                           Equipment
                                               - r--
                                               = F=>
                                                       Trip
                                                       Coil
                                                              I-   ..   Circuit
                                                                        Breaker
                                                                        Mecha-

      -• =I TE t=
                                                                         nism

                                                         f
               1                   t                     I                  ...

                            DC-System

                 Fig. 2.1 The fault clearance system

2.2   BACK-UP PROTECTION
All elements in the fault clearance system do not always operate correctly.
Protection relays may fail to operate or may operate when they are not required to
operate. Switching devices may fail to interrupt the fault current. Common practice is
to use several protection systems operating in parallel. Back-up protection is
intended to operate when a power system fault is not cleared, or abnormal condition
is not detected, in the required time because of failure or inability of other protections
to operate or because of some other fault in the main fault clearance system e.g.,
broken wire in cable from PT, broken wire in the cable from relay to the CB trip coil
or failure of the appropriate circuit breaker(s) to trip.

       By providing back-up protection, it is possible to reduce the risk arising out of
situation when a protection relay or a switching device fails to operate. The back up
protections can be classified as under.

•     Remote back up.
      The main protection and the back-up protection may reside in different
      substations
•     Local back-up
      The main protection and the back-up protection reside in the same substation.
      The local back up protections can be further classified as under.

8                 Manual on RsliabIB Faun C/sarancs and Back-Up Protection of
                             EHVand UHV Transmission Networlrs

            Circuit local back-up protection
            The protection senses the same current and voltage as the main
            protection.
            Substation local back-up protection
            The protection uses current different from the one used by the main
            protection.

       Ideal back-up protection should be completely independent of the main
protection. Current transformers, voltage transformers, auxiliary tripping relay, trip
coils and auxiliary DC supply systems should be duplicated. This ideal condition is
rarely attained in practice. The following compromises are usually made:

•     There is only one current transformer but it has several cores. One core and
      its associated secondary winding energise each protection. Some times one
      CT secondary winding feeds more than one protection.

•     Common voltage transformers are normally used because duplication would
      involve a considerable increase in cost, because of the voltage transformers
      themselves, and because of the increased space that would have to be
      provided. Since security of the VT output is vital, it is desirable that the supply
      to each protection is either from separate cores or separately fused as close
      to the VT as possible and continuously supervised by a relay that will give
      alarm on failure of the supply and, where appropriate, prevent an unwanted
      operation.

•     Trip supplies to the two protections should be separately fused. Duplication of
      tripping batteries and of trip coils on circuit breakers is sometimes provided.

2.3   REMOTE BACK-UP PROTECTION
Remote back up protection is the ideal form of back-up protection, in systems where
it can function properly. Second and third zones of distance relays are examples of
remote back up. Sometimes variations of the in feed at the remote bus bars may
virtually prevent the application of remote back-up protection.

      The advantage of remote back-up is that it is completely independent of the
protection relays, current transformers and voltage transformers of the main
protection system. It is also independent of the auxiliary DC supply system and the
breakers in the substation. There are hardly any hardware failures that can affect
both the main protection and the back-up protection. The setting of Remote Back-up
protection relays to cover the fault outside the first zone of protection beyond the
remote bus bars due to infeeds to the fault from other parallel sources are quite
complicated and sometimes less selective.

                                  Chapter 2: Fundamentals                            9

2.4   CIRCUIT LOCAL BACK UP PROTECTION
The circuit local back up protection uses the same current and voltage as the main
protection. Delayed directional or non directional over current and earth fault relays
that are provided in the same circuit are examples of circuit local back up protection.

2.5   SUBSTATION LOCAL BACK UP PROTECTION
A substation back up protection is a time-delayed protection provided in the same
substation but normally fed by a CT different from the one feeding the main
protection. Over current protections provided in the incoming feeders providing back
up to protections in the outgoing feeders in a substation is one example of
substation local back-up protection. It must be noted that in a meshed network it
may be difficult to obtain back up protection of EHV lines by means of substation
local back up protection.
      In EHV substations it is possible to provide substation local back up protection
by reverse looking elements of distance relay.

       A                                                                        B

                    1                                                1

                    4                                                4

                Fig. 2.2 Duplicated main protections

2.6   DUPLICATED MAIN PROTECTIONS
In EHV and UHV networks it is common practice to use duplicated line protections,
viz.: Main1, Main 2 protections. Since the current transformers, the voltage
transformers and the breakers are the expensive components in the fault clearance
system it may be difficult to justify the cost for their duplication. Figure 2.2 shows
example of modern line protection arrangement suggested.
•     Block-1 in Figure presents the first main protection, Main-1
•     Block-2 represents the second main protection, Main·2.

10                 Manual on RsliabIB Faun C/sarancs and Back-Up Protection of
                              EHVand UHV Transmission Networlrs

•       Block-3 represents the teleprotection equipment for Main-1
•       Block-4 represents the teleprotection equipment for Main-2
•       Block-5 represents the telecommunication equipment for Main-1
•       Block-6 represents the telecommunication equipment for Main-2.

2.7     BREAKER FAILURE PROTECTION
Breaker failure protection is part of the local back-up protection. The breaker failure
protection has to trip the adjacent breakers when the main breaker does not
interrupt the fault current. The most common, and simplest, breaker failure
protection consists of a timer, which the protection starts when it operates. If the
fault current persists for longer time than the setting of the timer, the breaker failure
protection gives a trip command to adjacent breakers. Figure 2.3 shows the basic
decision process in any breaker failure protection. The retrip signal shown here is
optional.

                         No      Normal                                       eset 8reake
                                Operation                                       Failure
                                                                               Protection

                                   Start
                                  Breaker               Wait for
                                  Failure                 Fault
           Yes                   Protection            Clearance

                                              Retrip
                                                                                    No

                                    Trip
                                  Main                                            Trip
                                Breeker(s)                                      Adjacent
                                                                               Breaker(s)

                  Fig. 2.3 Flow diagram for breaker failure protection

2.8     RECOMMENDATION               FOR      APPLICATION                OF      SINGLE     FAILURE
        CRITERION
It is recommended to apply the single- failure criterion in the planning of the fault
clearance system. An elementary form of the single-failure criterion requires that the
failure of anyone component in a fault clearance system should not result in a
complete failure to clear a power system fault or abnormality. The single-failure
criterion can be applied as follows:
•     Assume that the power system is either in its normal switching state or that one
      line is out of service.

                                Chapter 2: Fundamentals                           11

•   Assume that a power system fault occurs on the power system. Consider the
    following types of faults.
            Three-phase fault
            Phase-to-earth fault
            Phase-to-phase fault
            Open conductor or broken conductor fault
    Assume that there is a fault in the fault clearance system (in substation
    elements). Consider one of the following types of faults in the fault clearance
    system.
            Loss of input from a voltage transformer,
            Loss of input from a current transformer,
            A failure to operate of a protection relay,
            A blown DC fuse,
            An interruption of a tripping circuit
            A failure of remote end communication (especially line differential
            protection)
            A failure to operate of a switching device.

•     Check if with the above fault(s), the fault clearance system clears the power
      system fault at pre-defined locations considering the following types of faults
      on system elements:
            A line fault
            A bus bar fault
            A fault in power transformer
            A fault in the shunt reactor

     Add second main protection or back-up protection until the fault clearance
system clears al the faults.

•     Check if the healthy lines and healthy items of plant can withstand the fault
      current for the above cases. Add second main protection, back-up protection
      or reinforce the primary equipment until it withstands the fault current during
      the fault clearance time.

      The protection engineer must carry out a more detailed analysis to check the
above cases under different outage conditions for which the system has been
planned. Examples of outages to be considered are outage of a line, outage of a
power transformer, outage of a generator etc.

## Chapter 3: Requirements

REQUIREMENTS
      The protection engineer has to understand requirements that are expected
from the protection system before deciding the arrangements for it. Here the
requirements can be grouped under two categories:
•     External requirements
•     Power system requirements

3.1   EXTERNAL REQUIREMENTS
External requirements for protective systems encompass a wide range of non-
technical considerations put on the protection engineer by some external authorities.
These considerations fall in the following six categories:
•     Requirements imposed by various govemmental and other agencies
      regarding safety.
•     Requirements imposed by manufacturers of the primary equipment in order to
      validate equipment warranties.
•     Requirements by insurance companies who underwrite equipment failures.
•     Legal requirements to meet "prudent utility practice and industry standards" in
      the event that primary equipment failures result in personal injury or property
      damage and legal action is taken against the utility by the parties incurring
      damage.
•     Requirements for the safety grounding systems.
•     General power quality requirements from the customer

      Some of these requirements may not be imposed or felt at present by the
protection engineers in India. But as and when these are introduced by the
concerned authorities to meet the requirements of the system as a result of
deregulation and restructuring coming into force, the appropriate protection
application commensurate with the changed environment will have to made by the
concerned authorities. The following paragraphs give some more details of these
requirements.

3.1.1 Safety Regulations
Electrical Safety Regulations may require some back-up protections. These
requirements are intended to meet the minimum requirements associated with public
safety.

14                 Manual on Reliable Faun C/sar.mce and Back-Up Protsction of
                              EHVand UHV Transmission Networks

3_1_2 Equipment Warranties
Utilities may obtain warranty as a part of purchase agreements. The manufacturer
has the responsibility to replace damaged equipment and may require the utility to
provide a minimum level of protection.

3.1.3 Insurance Requirements
Devices may be covered by insurance. The insurance companies pay the cost of
replacing failed equipment and may require minimum levels of protection.

3.1.4 Industry Standards
In some cases personal injury and property damage liabilities are decided in court.
The court's decision may be based on a review of protection standards. If the utility
has not met the minimum levels of protection, they may be held liable for the
appropriate damages.

3.1.5 Prudent Utility Prectice
Another common case against the utility is based on a review of prudent utility
practice. If one utility uses lower levels of protection than other utilities, it is argued
that the utility is not following prudent utility practice and they may be held liable for
the appropriate damages.

3.1.6 Safety Grounding
Care is to be taken to provide for appropriate step and touch potentials during
ground faults as also control circuit transients associated with fault switching or even
normal operations. Short clearance time is advantageous because the risk of electric
shock is greatly reduced and the risk of severe injury or death is greatly reduced if
the duration of a current flow through the body is very brief.

3.1.7 Power Quality
Power quality requirements are changing as competition increases. Potential
customers will start asking for reliability data of the electricity supply before they
establish new plants. Some process industries cannot tolerate even very short
system disturbances.

3.2   POWER SYSTEM REQUIREMENTS
In general protection system criteria must meet the planning and operating criteria
requirements while meeting the specific requirements of the power system element
being protected and preventing damage to other power system elements supplying
fault current.

                                Chapter 3 : Requirements                              15

      Over tripping of protective system must be limited to events where more than
(n-1) dimensioning can be tolerated by the system. Failure of the protective system
to operate during fault events must be eliminated by using appropriate back up
protection to fulfill the requirement of planning criteria.

      Duplicate protection and back-up protection must meet all of the design
requirements of the planning criteria at a minimal cost.

3.3   NORMS USED TRANSMISSION PLANNING IN INDIAN POWER SYSTEM
The planning and operational requirements and security standards for the purpose
of transmission planning for Indian power system are brought out in the Document
titled "Manual on Transmission Planning Criteria" issued by Central Electricity
Authority, New Delhi in 1992 and this may be referred for more details. This
document may be further subjected to revisions for updating in view of system
expansion.

3.4   PROTECTION CRITERIA
Protection criteria are developed and derived from the Planning and Operating
Criteria. The purpose is to meet the dimensioning requirements associated with
faults so as to prevent loss of stability, loss of synchronism, voltage collapse,
undesired load shedding or unacceptable frequency and voltage excursions. Some
utilities may want to do preventive maintenance with the primary equipment in
service.
        Utilities may desire to provide for loss of one system element (such as
equipment failure) during peak load conditions. If this be the case such planning
criteria should be made known to the protection engineer. It is vital that there is very
close collaboration between the planning and protection engineers at the very early
stages of the projects to identify the protection requirements for the envisaged
projects.

     There are three types of criteria, as mentioned below, that the protective
system must meet.
o     Criteria specific to the equipment within the protective zone must be met.
      These are construction specific requirements such as tank rupture
      requirements of capacitor cans.
o     Criteria specific to other equipment supplying fault current to the faulted
      element. These are fault current withstand requirements such as the
      maximum fault current duration of a power transformer.
o     Criteria specific to the stability of the network. These are topology specific time
      limits associated with voltage and transient stability.

16                Manual on Reliable Faun C/sar.mce and Back-Up Protsction of
                             EHVand UHV Transmission Networks

       Power system faults subject the power generating units to voltage excursions
and dips. If the power system fault occurs close to the large power stations, there is
a risk that many power generating units could get disconnected from the
transmission networks. This means that a correctly cleared fault may cause an
outage if the power-generating unit does not withstand severe voltage dips. Back-up
delayed clearance of a power system fault close to the power plant may cause a
severe outage. General voltage stability requirements determine the duration of the
fault and are system configuration dependent.

3.5   FAULT CURRENT WITHSTAND CAPABILITY
No utility can specify that the power system elements specially CT, Isolators and
circuit breakers besides the power transformers shall withstand only fault currents
associated with normal fault clearance and take the risk of circuit breaker failures.
The system elements are usually specified to withstand the fault currents associated
with back-up clearance times of 0.5, 1.0 and 3.0 seconds

       The power system elements must withstand both normal rated load currents
and fault currents specified. The rated peak withstand current and the rated short
time withstand current characterize the components. Fault currents are usually small
in the initial stages of development of power system. Normally, the magnitude of the
fault current increases as the system develops. The magnitude of fault currents
influences the dimensioning of the power system components like transformers,
circuit breakers and other primary equipment. High short circuit currents affect
primarily the mechanical and thermal dimensioning of the power system
components.

       The fault clearance system cannot normally influence the peak value of the
fault current. The properties of the fault clearance system can, however, influence
the duration of the fault current. Thus, the fault clearance time influences the heating
of conductors during disturbances. The protection engineer must know how long the
power system components can withstand the fault currents without permanent
damage. In general, the components of the power system are specified to withstand
the fault current duration associated with back-up fault clearance as specified in
national and international standards. For example, transformer through fault
capability is outlined in ANSI/IEEE C57.12.00 and IEC Publications 76-5.

       The requirements in respect of Indian Power System for fault withstand
currents of the power system elements are brought out in the document entitled
'Manual on Transmission Planning Criteria" of Central Electricity Authority, New
Delhi. Some details from this are reproduced below.

                                       Chapter 3 : Requirements                               17

Table 3.1 Rated breaking current capability of switchgear at different voltages

           System voltage                       FauHlevel                         Duration
                132 kV                          25/31.5kA                         1 13 Sec.
                220kV                           31.5/40 kA                          1 Sec.
                400kV                            40/63kA                            1 Sec.
                765kV                             40 kA                             1 Sec.

3.6    RECOMMENDATIONS FOR SYSTEM PLANNERS AND PROTECTION
       ENGINEERS
For reasons brought out above, it is recommended that the system planners and
designers assess the requirements for 132 kV, 220 kV, 400 kV and 765 kV systems
and coordinate with the protection engineers to ensure that these requirements are
fulfilled. Sometimes such requirements may have to be studied on case-to-case
basis where general guidelines may not be sufficient to meet the system
requirements and suitable measures taken. In view of rapid generation expansions
there could be certain locations in generation complexes where fault level may
exceed the specified short time current rating. In such cases suitable measures are
required to be taken by the system planners to contain and limit the fault current
through effective use of Fault Current Limiters.

## Chapter 4: Performance Indices

PERFORMANCE INDICES
The task of fault clearance system is to detect power system faults and
abnormalities, identify the faulty item of the plant, and interrupt the fault currents as
quickly and reasonable. In order to assess quantitatively the reliability of fault
clearance systems, there have to be a set of performance indices. For this purpose,
certain indices for protection devices and switching devices are recommended and
these are described below.

4.1   CORRECT PERFORMANCE
To describe what is meant by correct performance and what is incorrect
performance by a protective system consider the following three cases :

•     Consider a fault in the power system for which the protection system provided
      should operate. If the protection system operates and issues a correct tripping
      command, it should be taken as correct performance and if it does not issue
      tripping command and operates incorrectly it should be taken as incorrect
      performance

•     Consider a fault in the power system for which the protection should not
      operate. In this case the protection system operates incorrectly if it issues a
      tripping command and it operates correctly if it refrains from issuing a tripping
      command.

•     Consider a case when neither a power system fault nor an abnormality exists
      and therefore the protection should not operate. In this case the protection
      system operates incorrectly if it issues a tripping command and it operates
      correctly if it refrains from issuing a tripping command.

4.2   DEPENDABILITY OF PROTECTIONS
The dependability of protection is defined as the probability for a protection of not
having a failure to operate under given conditions for a given time interval. An index
of dependability should measure the ability of the protection system to operate when
there is a power system fault for which the protection shall operate.

      Index, D of dependability is defined as follows:

                    N
      D = 1- _N_f = cc:,-'_-ccN:'-f   N,
                Ns     Ne +Nf

20                Manual on Reliable FauN C/eatanca and _-Up Protaction of
                            EHV and UHV Transmission Networl<s

      Here

      N, is the number of failures to operate at internal power system faults

      N. is the number of internal power system faults

      No is the number of correct operations during the given time interval.

      The performance index D is to measure the performance of protection when
there is a power system fault.

4.3   SECURITY OF PROTECTIONS
The Security of protection is defined as the probability for a protection of not having
an unwanted operation for a given time interval. An index of security should
measure the ability of the protection not to operate when it should not.

      Index, S of security is defined as follows:

      s=     N,
         Nc+N,.
      Where

      No is the number of correct operations

       N, is the number of unwanted operations of the protection during the given
time interval.

       Here N, is sum of N" and N". where N,. is the number of unwanted
operations of the protection in a given time interval without any power system fault
or abnormality and N" is number of operations of a protection in a given time
interval when there is a power system fault or abnormality for which protection
should not have operated.

      The performance index, S is to measure the ability of protection of not having
an unwanted operation in a given time interval. It measures the performance of
protection both when there is a power system fault or abnormality and when there is
no power system fault.

4.4   RELIABILITY OF PROTECTIONS
The reliability of a protection system is defined as the probability that a protection
can perform a required function under given conditions for a given time interval. The
reliability of protection is the ability of not having an incorrect operation. It is the
combined ability of not having a failure to operate and of not having an unwanted
operation.

                              Chapter 4 : Pelformance Indices                       21

      Index, R of reliability is defined as follows:

               N,
      R

      where,
      No is the number of correct operations
      N; is the number of incorrect operations during the given time interval.

      Here N; is sum of N, and Nu, where N, is the number of failures to operate on
internal power system faults in a given time interval and Nu is the number of
unwanted operations of the protection during the given time interval.

4.5   DEPENDABILITY OF SWITCHING DEVICES
The dependability of a switching device is defined as the probability of not having a
failure to interrupt the fault current when the device has received a trip command

      The dependability of a switching device is defined as follows:

               N,
      D

      where

      No is the number of correct responses when the device has received an
operate command.

      N, is the number of failure to respond.

4.6   FAULT CLEARANCE TIME
The performance indices described above measures the probability of not having a
failure to operate, the ability of not having an unwanted operation and the probability
of breaking or making the fault current. The performance indices do not explicitly
measure the speed of operation. For measuring the speed of operation following is
suggested:

      Fault clearance time, T, is defined as:

      T, = Mru:{T,..J
      Where,i = L ..N

22                  Manual on Reliable FauN C/eatanca and _-Up Protaction of
                                  EHV and UHV Transmission Networl<s

       Here, Ttl is the fault clearance time at terminal (i) of the protected section, and
N is the number of terminals of the protected section.

      Equation below defines the fault clearance time, Tf.I at terminal (i) of the
protected section:

      Here, T,.I is the operating time of the protection system at terminal (i), and Tb.l
is the operation time of the switching device at terminal (i). When necessary, T"
includes the operating time of the teleprotection channel.

      Figures 4.1 and 4.2 illustrate the concept of the fault clearance time, T t and
the fault clearance time, Ttl at the terminal (i) of the protected section.

4.7   TYPICAL EXAMPLE FOR CALCULATION OF VARIOUS PERFORMANCE
      INDICES
Performance of Transformer and Reactor protections during a given time interval

                   Type 01 operation                              Number of operation

        Correct operation (N,)                                            130

        Incorrect operation (N w )                                        3

        Failure to operate (Nil                                           0

         Operation causing non-power system                               17
              fault tripping (N,,)

                                            N,          130
                 Dependability, D                                 1.0
                                          N,+N j       130+0
                Security, S =       Nc
                                                N,                130
                                                                        0.867
                                  Nc+NH      Nc+Nu+ N ..       130+17+3

                                                                     130
                                                                                  0.867
                                                                 130+0+17+3

                                           Chapter 4 : Pelformance Indices                                       23

                               A                                                                       B

                                                                                                                 E,

                                                                    D                    F

                                                                          c
                                                                         z,

                                                                    - E,

                     Fig. 4.1 Single-line diagram for three-terminal line

         200
                     Fault current at A
                                                           ~
                                                                              ITf,11                   J
         150
                     Fault current at B
                                                       /'ITf,~~1
         100
                                                                              [Tf]
                                                  ~

                     Fault current at C
                                                                                              I
          50

                                                           f\
                     Current in the fault
                                                                             /\               ~
           o                           V               /        \        /     \         /"- '--./
                                                  V                 V              "-/
         -50
               -20                 o              20                40             60             80       100

                     Fig. 4.2 The fault clearance times, T,and Tf,i.

4.8   RECOMMENDATIONS FOR MEASUREMENT                                                    OF       PERFORMANCE
      INDICES AND ACTIONS FOR IMPROVEMENT
It is recommended that utilities have a system of measuring and keeping record of
the performance indices for:
•     Protection devices
•     Switching devices
     This can be valuable data for taking decisions regarding maintenance,
modernizing and retrofitting of switching and protection system.

24               Manual on Reliable FauN C/eatanca and _-Up Protaction of
                           EHV and UHV Transmission Networl<s

       It is recommended that once this practice is adopted and sufficient data is
collected, a system of benchmarking the indices be introduced by utilities and
actions be taken for improvement as considered necessary. The approach should
be to compare the indices collected in a particular period with the targets set,
analyse why there are differences and what actions can be taken to bridge the gaps
and then take actions for improvement. These actions can be regarding revision in
relay settings, better maintenance practices, modernizing and retrofitting of
switching and protection system etc, as felt appropriate. The targets can then be set
higher and further actions be taken for improvement.

       While evaluating this data apart from looking at protection devices and
switching devices, attention should also be given to remaining part of the fault
clearing system viz., D.C. supplies, teleprotection signaling, healthiness of tripping
cables, termination etc. This will help to improve the design of fault clearance
system.

## Chapter 5: Lines and Cables

LINES AND CABLES
In protection of transmission lines both dependability and security of protection are
of paramount importance. Any uncleared fault may create unwanted tripping and
lead to grid disturbances.
       Transmission circuit back-up protection caters for failure of any main
protection system to clear any fault that it is expected to clear. A protection function
that offers back-up for most faults may also provide main protection for some fault
conditions. However there could be some known limitations of the operating
principles of the main protection having restrictions in relay settings that could be
applied to the main protection.
      Two main protections could be justified on the basis of being able to keep an
important transmission circuit in service with one set of protection remaining in
service while second set of protection is taken under maintenance. Where two main
protection systems are justified one may take the opportunity to select main
protection systems that cover each other's limitations.
       The requirements of overhead line and cable protection systems vary greatly,
due to the exposure of transmission circuits to a wide variety of environmental
hazards and are subjected to the wide variations in the format, usage and
construction methodologies of transmission circuits. The type of protection signaling
(teleprotection) or data communication systems required to work with the protection
systems will also influence protection scheme requirements.
     As discussed in chapter 2, back-up protection might be provided in one or
more of the following forms.
•     Circuit local back-up.
•     Substation local back-up.
•     Remote back-up.

5.1   TYPICAL TRANSMISSION CIRCUIT ARRANGEMENTS
This section offers a brief overview of common transmission circuit arrangements
and physical construction factors which might have some influence on the exposure
of transmission circuits to faults and therefore on the selection of back-up protection
schemes. Transmission circuit construction can be considered in three main
categories.
•     Overhead construction.
•     Underground cable construction.
•     Composite construction.

26                Manual on Reliable FauN elBa"""", and Back-Up _   of
                             EHVand UHV Tnmsmission N9Iwot1rs

5_1_1 Overhead Transmission Circuits
Physical arrangements for overhead conductor support vary depending on voltage
level and cost considerations.

       The electrical parameters of resistance, reactance and capacitance are mainly
influenced by the size and type of conductors, conductor configuration and geometry
with respect to each other and with respect to ground along with the earth wires on
top of towers

       The thermal balance of electrical heat input and heat dissipation governs
circuit load current capacity. Heat inputs are from 12R losses, solar radiation and
solar conduction. Heat dissipations are through radiation and conduction, which
depends on ambient temperature, wind velocity and chill factors.

       Use of correct line parameters is important for proper setting of protective
relays. Calculation of overhead line electrical parameters at nominal system
frequency and line surge impedance are usually performed using dedicated
computer software. These calculations may then be verified by carrying out
measurements on final installations that could be subjected to field testing, as
ground conduction effects influence the zero sequence surge impedances. This
information may then be used by protection engineers to determine optimum relay
settings. The CIGRE WG 34.04 report titled "Application guide on protection of
complex transmission network configurations· gives details of how the
measurements of line impedance for the setting of distance protection and fault
locators can be carried out.

5.1.1-1 Ground WIres
Ground wires help to reduce the apparent tower footing resistance. It may be noted
that all HV, EHV and UHV lines need one or more than one ground wires at a
certain height above the conductors to provide the desired shielding The tower
footing impedance parameters are required to be kept as low as practically feasible
and may need special measures like counterpoises and other known methods of
reducing the footing impedances.

      The economic justification for ground wires, the number of ground wires
required and their geometry is mainly determined by ground flash density, keraunic
levels and severity of lightning surges as also topology of the line profile and tower
heights.

       Besides reducing the number of lightning induced faults, ground wires also
help to reduce the apparent tower footing resistance seen during conductor
flashover to ground causing ground faults. They provide multiple ground fault current
return paths through many tower footings, which helps in this. The annual outage
rate of the transmission line is required to be as low as possible

                               Chapter 5 : Unes and Cables                         27

     As said earlier individual tower footing resistances can be substantially
reduced by the use of counterpoises, which are generally of steel conductors buried
under each tower with several configurations in crowfoot layout or continuous
counterpoises connecting two or more number of towers in a row. This is usually
done where soil resistivity is very high.

       Even with ground wire shielding, a lightning strike to conductors or to earth
wire or to tower peaks of a line may cause an insulator back-flash over leading to
line outage. This is due to discharge current flowing through tower impedance and
tower footing resistance, which will result in a transient tower voltage rise with
respect to power line conductors. Such voltage rise could be sufficiently high to
cause a single or a multi-phase back-flash from a tower to its power conductors. It is
important to appreciate that where a high transmission tower is erected on high
profile ground with high tower footing resistance, ground wires may increase the
lightning outage rates. The transmission line designers cover this aspect while
designing the tower and conductor configuration and Bil of insulator strings. To
minimize the risk of outages there should be good coordination between Bil of
insulator strings and tower footing resistance.

5.1.2 Underground Transmission Circuits
The electrical characteristics of HV and EHV cables for underground transmission
circuits to carry a given load are set by the physical configuration of the conductors
and the properties of the insulating media, which materially affect the capacitance of
the cable. The materials used and the voltage rating determines the external
diameter and the weight of a cable. Heat dissipation within a cable is predominantly
through 12R load current losses and this is normally dissipated by conduction through
the dielectric to the soil in which the cable is buried. Cooling may be enhanced by
special back-fills in cable trenches. Internal cooling for EHV Cable may be obtained
by circulating oil through hollow conductors or through other ducts within the cable.
Cables are assigned a continuous load current rating at reference environmental
conditions.

       Cable shunt capacitance per unit length is much higher than for overhead
lines. Charging currents increase with cable voltage ratings. This means that
inductive shunt compensation is commonly required for EHV cables and also for
unusually long HV cables. A good example of such a scenarios could be seen from
the parallel cable rings at 400 kV in Berlin provided by Power Utility BEWAG and
also in the National Grid of UK.

       Being less prone to fault-inducing environmental hazards than overhead lines,
cable faults are almost exclusively permanent faults. Consequently, automatic
reclosing is not used for underground transmission circuits. In cable circuits, faults
can also occur in associated switchgear and cable joints. The level of incidence of
faults in these is oiten comparable to faults in the cable itself.

28                Manual on Reliable FauN elBa"""", and Back-Up _   of
                             EHVand UHV Tnmsmission N9Iwot1rs

       Cables do not withstand fault currents for long periods of time; consequently
they demand the use of protection without any intentional time delay. This is a
feature of unit protection, such as current differential protection, through pilot wires
or fibre optic cables, which is often applied to cable circuits.

5.1.3 Composite Transmission Circuits
Planning strategies and design requirements sometimes demand the creation of
composite transmission circuits. The typical composite circuit is a mix of overhead
and underground circuit.

       Although less frequent, there are cases of non-homogeneous radial overhead
lines, with different types of conductor or varying conductor geometry along their
route. This is often the case where a sub-transmission line supplies many teed
transformers, since it is possible to economize on conductor size as the circuit
loading decreases from the primary substation up to the most remote substation.

     With non-homogeneous series impedance for a composite circuit, especially
where cable sections are involved, there may be some difficulty in setting optimum
impedance settings for distance relays and in setting optimum residual
compensation for ground faults.

      Although the transmission lines are originally planned to interconnect two
substations after a period they are altered to suit changing requirements in the
transmission system. Often, the presence of multi-circuit lines, multi-terminal lines
and transformer tee-off's, are due to these reasons.

      In some cases, planning strategy may lead to a gradual implementation of
complex transmission arrangements. With long intervals between successive stages
of implementation, it is not always possible to engineer protection systems at each
stage that will suit the final configuration. When such changes take place it is
recommended that changing, refurbishing or upgrading of protection systems
harmonizing with the power systems already in operation, be carried out.

5.2   COMPLEX TRANSMISSION CIRCUITS
The following types of lines can be classified as complex transmission circuits that
often present special protection difficulties:

•     Parallel transmission lines where two or more three phase transmission
      circuits are arranged on the same tower or follow the same right of way on
      adjacent towers.

•     Multi-terminal lines having three or more terminals with substantial generation
      behind each.

                                Chapter 5 : Unes and Cables                            29

•       Tapped lines having one or more terminals with substantial generation behind
        them and taps feeding only the load. The tap is done through a step-down
        transformer and do not have sufficient current feedback to operate the relays.

•       Composite lines where system elements like transfonmers, overhead lines or
        cables are connected together without intermediate circuit breakers.

•       Series Compensated lines

       The protection of these complex transmission lines is very well described in
the document produced by CIGRE WG 34.04 in 1991 titled - "Application guide on
protection of complex transmission network configurations".

5.2.1     Parallel Transmission Circuits
Often, for reasons of economy, two or more circuits are run in parallel on the same
towers. Transmission reliability is reduced in the event of multiple circuit faults
caused by lightning and certain common mode events, such as a tower collapse,
which result in sustained faults. If insulation back-flash occurs with a direct lightning
strike to a tower, it could result in multi-circuit faults resulting into outages.

       The possibility of multiple faults occurring simultaneously on more than one
circuit of a transmission network imposes special demands on protection in terms of
phase selection for single-pole tripping, that may affect high speed single phase
auto-reclosing.

       With double circuit tower construction, there is relatively strong inter-circuit
magnetic coupling between conductors, which is expressed in tenms of various inter-
circuit mutual impedances for the purposes of short-circuit calculations and analysis
of protection perionmance. It is usually acceptable to neglect the positive and
negative sequence mutual impedances, since they are only a fraction of the positive
sequence self impedances. It is sometimes necessary to consider the coupling from
the positive sequence network to the zero sequence network when setting sensitive
residual over current protections. Zero sequence mutual impedance should not be
ignored, because of its relatively high value and its possible influence on proper
ground fault protection of lines.

      The mutual coupling permutations that result from multiple circuits, which
share a common right-of-way, are complex in nature.

       Mutual coupling is not restricted to parallel circuits at the same voltage level or
to circuits which have two common terminals. In some cases circuits may run in
parallel for part of their route. Where there is a parallel run, two circuits might use
common, double-circuit support towers.

30                Manual on Reliable FauN elBa"""", and Back-Up _    of
                             EHVand UHV Tnmsmission N9Iwot1rs

       There are some cases of circuits at different voltage levels sharing the same
tower. This may lead to inter-system faults. Despite their severity, it may be very
difficult to discriminatively detect such faults with protection functions that are
dependent on voltage measurement. The appropriate phase selection difficulties are
even greater for these lines. Phase-segregated unit protection based on current
measurement is the best option for both circuits when it is economically and
technically feasible.

       The main consequence of the magnetic coupling between parallel overhead
lines is the modification of the zero sequence voltage profile during a ground fault on
one circuit. The zero sequence voltage profile along any circuit will not be entirely
dependent on the zero sequence current flowing in that circuit. Instead it will depend
on zero sequence current flowing in the parallel circuit(s).

      It follows that protection functions based on voltage measurement are those
most likely to be affected by zero sequence mutual coupling, as highlighted below:

•     Directional ground fault protection

      Zero sequence voltage and current signals are those most commonly
      employed by ground fault directional control elements. A ground fault on one
      circuit may cause operation of directional ground fault protection on a partially
      parallel circuit due to partial zero sequence mutual coupling. This problem
      does not exist for parallel circuits between common substation bus bars.

•     Distance protection reach accuracy

      The reach of distance protection ground fault elements is adversely affected
      by modification of power system zero sequence voltage profile through zero
      sequence mutual coupling. If zero sequence currents flowing in parallel
      circuits are of similar phase to the current in the protected circuits, ground fault
      distance elements will under reach. If the currents are virtually in anti-phase,
      the distance elements will tend to over reach.

      The tendency for distance protection to over reach is of no consequence for
distance elements, which are intended to overreach a protected line, such as Zones
2 or 3. Any tendency to under reach can be compensated for, when setting the over
reach elements. Consequently, all tele-protection schemes based on over reaching
elements are suitable for protection of magnetically coupled circuits, when set to
take into account under reaching during ground faults. However, where common
impedance settings exist for phase and earth fault impedance elements, it should be
noted that any compensatory increase in distance element over reach may make it
necessary to employ current reversal guard logic in a teleprotection scheme. Where
the over reaching elements are also used to provide Zone-2 back-up protection for
end zone faults, a compensatory increase in reach may also create discrimination
problems with phase to phase fault protection for short adjacent lines.

                               Chapter 5 : Unes and Cables                          31

       A potentially problematic case of Zone-I overreach to be noted is when a
parallel circuit is switched out and grounded at both terminals. In such an instance,
the Zone-1 reach security margin may be greatly reduced or it may even become
negative in some applications.

      One of the methods to compensate for the effect of zero sequence mutual
impedance is to take zero sequence current signal from the parallel circuit and use it
to provide compensation. This technique is not effective when parallel circuit is
disconnected and grounded at both ends. For this reason this method is not used for
protection but used for fault location.

       In general, it is not advantageous to introduce mutual compensation for
distance protection schemes. The advantages, if any, are usually far outweighed by
the problems and operational complexities that would be introduced. Most distance
protection schemes can be set to provide fast tripping for faults along a multi-circuit
line and be stable for external faults without employing mutual compensation. There
are also applications where it is impossible to access the current from a magnetically
coupled circuit at one or both terminals. In all such cases the maximum reach of first
zone setting fixed as 80% or less could be advantageous.

      An alternative to implementing mutual compensation is to apply individual zero
sequence compensation factor for each zone of ground fault distance protection.
Another option is different groups of setting parameters for different operating
conditions of the double circuit line.

       From the above it transpires that correct calculation of the transmission line
impedance matrix with zero sequence parameters be carried out and proved by field
tests before using them in setting the relays.

5.2.2 Multi-terminal Transmission circuits
Whenever a transmission circuit has three or more terminals, its protection may be
subject to adverse effects within the protected line due to the effects of in feeds.
Depending on the protection operating principle, these effects may be a cause for
concern. Additional in feed can increase impedances seen by distance relays and
out feed can cause directional protection at one terminal to identify an internal fault
as external. Carrier-aided protection with efficient information links with judicious
application of correct measurands and protection relays should be applied

32                Manual on Reliable FauN elBa"""", and Back-Up _   of
                             EHVand UHV Tnmsmission N9Iwot1rs

5_2_3 Shunt Compensation
The distributed shunt capacitance of a transmission line can cause a voltage rise
when load is lower than normal load. This is termed as Ferranti Effect.

      Switched or non-switched shunt reactors are often used to compensate for
high levels of shunt capacitance for long overhead lines or for underground cables.
The shunt compensation is invariably located at terminal substations, where it may
be connected to the associated circuit by an isolator switch or by a circuit breaker.
The former option is less expensive, but it may be necessary to de-energise the line
to insert or switch-off the reactor. Sometimes shunt reactors controlled by circuit
breakers are connected to EHV bus bars. In many other cases, shunt reactors (and
many times Static Var Compensators with inductive and capacitive compensation
range are also connected to the tertiary windings of Interconnecting auto-
transformers (ICT) for control of downstream voltage profile. With expansion of
power network, many times the line lengths get shortened and intermediate stations
are connected with loop in and loop out (LlLO) connections. Under such conditions
the non-switched line reactors provided on the long lines are removed or replaced
by bus reactors. Under certain conditions it may be advisable to use the controlled
shunt reactor that could remain on the line for all conditions of operation. Such
application could be kept in view to provide minimum changes in reactor shifting.

      Shunt compensation equipment must have its own protective gear. Where a
shunt reactor is connected to a transmission circuit only by isolator switch, its
protection requires a fast and reliable transfer-tripping scheme in order to remove
remote-end fault current in feed.

       Shunt reactors do not have a great influence on the selection of line
protection, except where differential or directional comparison protection might be
responsive to live-line switching of reactors. In such cases, reactors may have to be
excluded from the zone of line protection through the use of reactor CT's in parallel
with line CT's. It may also be necessary to inhibit any reactor back-up ground fault
protection during single-pole auto reclose sequences.

      When single-pole tripping and autoreclosure is applied, capacitive and
inductive coupling may delay the extinction of the secondary arc and the faulted
phase voltage decay may be delayed. This is due to resonance between shunt
reactor inductance and the capacitance coupling to live phases after the breaker is
tripped. This may delay arc extinction for a transient fault and so single-pole
autoreclose dead-times may need to be extended for limiting the parameter of
secondary arc current to a practical value of about 10 amperes. A Surge Protected
Neutral Reactor usually of 0.2 to 0.4 pu ohmic value is connected between neutral of
EHV shunt reactor and the ground. This requires the ratio of zero to positive
sequence impedance of shunt reactor be around 0.9 to limit the BIL of shunt reactor
to around 550 kV in a 400 kV network.

                               Chapter 5 : Unes and Cables                           33

5.2.4 Series Compensation
As stability constraints limit the maximum value of power angle for long lines, the full
load current capacity can only be utilized if the transmission circuit impedance is
reduced. The surge Impedance Loading (SIL) of a transmission line, say 400 kV, is
around 515 MW while the thermal limit of the same line could be around 800 to 1200
MW under various operating conditions. This is further complicated by shunt
reactors directly connected on the lines that modify the SIL to about 70% of original
value. Such conditions always need extra capacitive vars if more power to the level
of its thermal capacity is required to be pushed into the line. The application of
series compensation on transmission lines is provided for such relief. Some of the
other reasons for applying series compensation could be to avoid voltage collapse,
to optimize load distribution or to improve quality of supply apart from improving
transient stability.

     Sometimes Thyristor Controlled Series Capacitor (TCSC) is used. Some of the
reasons for this could be power oscillation detection, prevention of sub synchronous
resonance or load flow control.

       Series compensation has been universally applied to lines at all the known
voltage level right from 11 kV to 800 kV .The protection relaying of such lines are
quite complicated and need to be evolved after detailed system studies.

      The combined effect of series capacitors and their protective current diversion
devices on line protection performance and the impact of series compensation on
protection of adjacent lines require detailed discussion and is not covered within this
document. Document produced by CIGRE WG 34.04 titled "Application guide on
protection of complex transmission network configurations" may be referred for this.

5.3   TRANSMISSION CIRCUIT FAILURE MODES AND RATES
The failure rate of transmission lines range from 0.2 to more than 10 faults per
100 km per year. The failure rate is a function of keraunic level, the insulation level
and the existence of many environmental factors such as vegetation proximity,
fouling with over·grown trees air pollution levels, vandalism and bush fires or fires on
crops waste created by the farmers below or very close to lines. Some of these are
described below.

5.3.1 Arcing Faults
Many types of fault-inducing events result in the creation of an arcing fault between
phases of a line, between phases and tower structures or between phases and
ground. Fault arcs present non-linear fault resistance. Estimates of fault resistance
based on arc length can be obtained using well-known Warrington formulae or
various other empirical formulas used in Europe.

34                 Manual on Reliable FauN elBa"""", and Back-Up _    of
                              EHVand UHV Tnmsmission N9Iwot1rs

5_3_2 Smoke Hazard
Accidental or deliberately initiated bush fires are quite common during certain
seasons. Burning of sugarcane waste close to transmission line is one such
example. Smoke from such fires may induce arcing faults as a consequence of air
ionization. Some faults may be located across insulators or between a pair of
phases and these will not differ much in nature from those initiated by lightning.
Others may be located at the mid-span between towers, from the lowest conductor
to ground. Such mid-span faults can be highly resistive, not only as a result of long
arc lengths, but also as a result of the ground resistance between the point of arc
and the nearest support towers.

      It may often be necessary to provide high resistance ground fault protection as
supplementary main protection in order to detect such faults, which may also act as
back-up protection for solid faults and is therefore recommended.

      Faults resulting from bush fires are usually non-damaging faults, with a good
chance of successful autoreclosure following fault clearance. But the effectiveness
of autoreclose schemes is frequently defeated by the intense ionization of the
insulating air in the vicinity of the fire, leading to new developing faults following line
re-energisation.

5.3.3 Vegetation Faults
There can be many line faults to ground, which are caused by rapidly growing
vegetation. Bamboo plant is one such example. From operational experience, such
faults are known to be of high-resistance. The fault presents itself as a very high
resistance to earth (of the order of several kilo Ohms), until the steam and smoke
produced by thermal energy dissipation in the tree resistance results in a tree-length
flashover. This occurs after several seconds.

       Ground fault elements of distance relays may not detect the high resistance
faults and the sensitive ground fault protection mentioned in the previous paragraph
can also take care of high resistance faults due to growing vegetation.

5.3.4 Forms of Overhead Line Faults
The failure rates of power lines vary from utility to utility and from year to year. The
most common type of fault is phase to ground fault (of the order of 75% or more)
and most faults are transient in nature. Since most faults involve ground,
consideration must be given to the levels of ground fault resistance that might be
encountered for particular applications and whether the main protection will be able
to detect all such ground faults. If not, supplementary protection may be required to
cover high resistance faults. The ground fault elements of distance relays should be
supplemented by a sensitive residual over current relay.

                                Chapter 5 : Unes and Cables                             35

5.4   TRANSMISSION CIRCUIT PROTECTION REQUIREMENTS
To determine the back·up protection requirements for transmission circuits it is
necessary at the first instance to identify the main protection requirements for each
of the system voltage level and then to identify application specific requirements in
relation to the protected circuit. Examples of possible main requirements are listed
below:
•     Maintaining transient stability of the power system
•     Maintaining operation of power station auxiliary system
•     Avoiding loss of supply to bus bars
•     Quality of supply
Examples of application specific requirements are listed below:
•     Allow for failure of a protection signaling/communication channel
•     Allow protection testing with the circuit in service
•     Protect a transformer feeder
•     Protect a tapped line through a step·down transformer
•     Protect a circuit with more than two terminals
•     Protect a circuit in series compensated network
•     Detection of broken conductors/jumpers of overhead lines.
•     Detection of high resistance faults on overhead lines
•     Operate within short·time thermal ratings of overhead lines and cables
•     Fault detection with weak or zero in feed from one circuit tenninal

     Combinations of main and back·up protection systems should be used to
address the main and application specific requirements for transmission circuits.

5.4.1 Maintaining Transient Stability
Common requirements for circuits at primary transmission voltages are the
maximum permitted fault clearance time in order to maintain system transient
stability. A single time limit is oiten quoted for a particular transmission voltage level,
but separate limits might be quoted for different fault types. On the basis that most
protection arrangements rely on a single protection system to clear different types of
solid fault, a single time limit is usually used as a main design requirement. An
exception sometimes exists to allow slower clearance of high resistance ground
faults that may not be severe in nature.
        It must be recognized that the maximum permitted fault clearance times
declared for a primary transmission system will not remain fixed. Power systems

36                Manual on Reliable FauN elBa"""", and Back-Up _   of
                             EHVand UHV Tnmsmission N9Iwot1rs

undergo constant evolution. In particular, the changes in the location, capacity and
design of generating plant that occur on most power systems demand constant
reviews by system planners of the maximum permitted fault clearance times for
existing transmission circuits. For EHV system the desired fault clearance time of 5
cycles that include the relay time, breaker time and carrier times is generally applied.
It may be desirable for EHV lines to have a maximum total-break time of circuit
breakers as 2 cycles (40 milliseconds) giving freedom to optimize the time of
protective relay and information links.

       When applying the single-failure protection design criterion, and where there
is a potential transient stability problem, a second protection system should be
provided which will clear faults within the maximum permitted time to maintain
transient stability. The back-up protection should also be fully discriminative, so that
tripping of more than one circuit does not further impair the power transfer capability
of the transmission system.

     This means that the second form of protection must be circuit-local and it must
have similar operating speed and discrimination qualities to those offered by the
main protection. This form of protection is referred to as second-main protection or
Main-2 protection.

      As discussed earlier, Main-2 protection is not generally regarded as being
back-up protection. The cost of this form of protection is easily justified in terms of
the single failure design criterion and the costs of possible system collapse resulting
from inadequate back-up protection performance. Any additional protection provided
as back-up to two main protection systems (M! and M2) would be back-up
protection for a dual failure criterion, where longer operating time limits would be
allowed.

5.4.2 Maintaining Operation of Power Station Auxiliary System
Depression of power supply voltages for auxiliary plant in some generating stations
may reduce the station output. Maintenance of full generation output may be a
critical power system security factor. In the case of nuclear plant, auxiliary power
supplies are also a major factor in providing full nuclear plant safety and security.

      The potential loss of system generation or the potential challenges to nuclear
plant safety systems may be factors which will dictate the longest acceptable
clearance times for transmission circuit faults in the vicinity of a power station.

5.4.3 Avoiding Loss of Supply
Where remote back-up protection or substation local back-up protection operates for
an uncleared fault on one transmission circuit, there will be a complete loss of
supply to the bus, which supplies the faulted circuit. In the case of multi-bus
substations (Double Bus, Breaker-and-Half bus bars, Double Main and Transfer bus

                               Chapter 5 : Unes and Cables                           37

or single bus or main and transfer bus substations), there will be loss of supply to
some step-down transformers, which mayor may not result in loss of supply to
consumers. There will also be loss of supply to any radially fed downstream
substations. In the case of a single bus arrangement, there will be a complete loss of
supply to local consumers. The costs of reduced supply capacity or total loss of
supply must be considered in relation to the cost of providing effective circuit local
back-up protection to avoid loss of bus supply.

5.4.4 Quality of Supply
A utility may enter into agreement with a large industrial consumer to limit the
duration of severe voltage depressions in order to secure a power supply contract to
industries like mining industry or costly continuous process industry. Quality of
supply considerations may influence decisions not only about the form of back-up
protection to be applied to a power system but also other add-ons such as dynamic
voltage supports and needs to be reviewed as and when these demands are made
by consumers on a case-to-case basis.

5.5   PROTECTION SCHEMES
The decision of whether or not to provide transmission circuit back-up protection, or
the level of back-up sophistication required, must be related to the cost of failure of
main protection to clear a fault which it is expected to clear and to the exposure to
such a cost. This means the decision to provide Main-2 protection for example
should not be merely based on voltage level but on how important the circuit is and
what it costs, if a fault on the circuit is not cleared in time. This concept could very
well applied to 220 kV and even at 132 kV levels

       Some consideration must be given to performance of main protection for
complex fault conditions, such as evolving faults, simultaneous faults and inter-
system faults. Where such faults are possible, but are of low probability, there may
be a need to provide back-up protection to cover for any identified credible
limitations of the main protection system(s). This aspect should be examined on a
case-to-case basis.

      In order to determine transmission circuit back-up protection requirements it is
necessary to understand and examine all possible modes of failure and any fault
detection limitations for main protection schemes.

       Listed below are schemes that are normally applied in India. Some of the main
attributes and limitations in the schemes are also listed under them. When applying
these schemes it is essential that the main attributes and limitations of are fully
examined and understood.

38                  Manual on Reliable FauN elBa"""", and Back-Up _   of
                               EHVand UHV Tnmsmission N9Iwot1rs

5_5_1     Distance Protection (Without signaling channel)
5_5_1_1 Multizone Distance Protection (With Three or More Zones)
Attributes
•       Fast tripping at both ends for about 60% of the protected line
•       Offers remote back-up protection
•       Offers substation back-up (Offset Z3 or Z4)
•       Can be phase selective
•       Communications independent tripping
•       Application to multi-terminal lines
•       Suitable for large in-zone loads
•       Suitable for transformer feeders
•       Suitable for composite circuits (lines/cables)
Limitations
•       Delayed tripping at ends of the line (for about 40% of protected line)
•       Limited resistive fault coverage
•       Dependent on VT signals
•       No weak end in feed I open terminal tripping
•       No detection of series faults
•       Many designs can be directionally unstable for series compensated lines
•       Zone 1 reach problems for series compensated lines
•       Lack of discrimination for faults between circuits of different voltage levels

5_5_2 Distance Protection (Signal Aided)
5_5_2_1 Accelerated under reach distance protection
Attributes
•       Communication independent fast tripping at both ends for about 60% of the
        protected line
•       Accelerated tripping at one end for faults in about 40% of the protected line
•       Offers remote back-up protection
•       Offers substation back-up (Offset Z3 or Z4)
•       Can be phase selective

                                 Chapter 5 : Lines and Cables                         39

•    Suitable for large in-zone loads
•    Suitable for transformer feeders
•    Suitable for composite circuits (lines/cables)
Limitations
•    Delayed tripping at ends of the line with 80% Zone 1 reach setting (for about
     40% of protected line) in case of communication failure
•    Resistive fault coverage limited by Zone 1
•    Not always suitable for multi terminal lines
•    Dependent on VT signals
•    No trip acceleration signal from weak end in feed / open terminal tripping
•    No weak end in feed / open terminal tripping
•    No detection of series faults
•    Many designs can be directionally unstable for series compensated lines
•    Zone 1 reach problems for series compensated lines
•    Lack of discrimination for faults between circuits of different voltage levels

5.5.2.2 Permissive under Reach Distance Protection

                                                                         Zcne-2
                                                Zcoe-1

                           9          SM<EXffiru<EX
                                       SlG-WlJr\G UN<
                                                          \t\ 9~
                           §J::::::::::::::::::::::::::::::::::::§]
                             I                                       I    I

                                                                          !

              ZDne-2

                Fig. 5.1 Permissive underreach distance protection

40               Manual on Reliable FauN elBa"""", and Back-Up _   of
                            EHVand UHV Tnmsmission N9Iwot1rs

Attributes
•    Communication independent fast tripping at both ends for about 60% of the
     protected line
•    Accelerated tripping at one end for faults in about 40% of the protected line
•    Offers remote back-up protection
•    Offers substation back-up (Offset Z3 or Z4)
•    Can be phase selective
•    Suitable for large in-zone loads
•    Suitable for transformer feeders
•    Suitable for composite circuits (lines/cables)
Limitations
•    Delayed tripping at ends of the line (for about 40% of protected line) in case of
     communication failure
•    Resistive fault coverage limited by Zone 1
•    Not always suitable for multi terminal lines
•    Dependent on VT signals
•    No trip acceleration signal from weak end in feed I open terminal tripping
•    No weak end in feed I open terminal tripping
•    No detection of series faults
•    Many designs can be directionally unstable for series compensated lines
•    Zone 1 reach problems for series compensated lines
•    Lack of discrimination for faults between circuits of different voltage levels

5_5_2_3 Intertrlpplng under Reach Distance Protection
Attributes
•    Communication independent fast tripping at both ends for about 60% of the
     protected line
•    Accelerated tripping at one end for faults in about 40% of the protected line
•    Offers remote back-up protection
•    Offers substation back-up (Offset Z3 or Z4)
•    Can be phase selective
•    Suitable for large in-zone loads
•    Suitable for transformer feeders
•    Suitable for composite circuits (lines/cables)

                              Chapter 5 : Unes and Cables                             41

•    Suitable for multi-terminal lines where all faults can be seen by Zone-1 from at
     least one terminal
Limitations
•    Delayed tripping at ends of the line (for about 40% of protected line) in case of
     communication failure
•    Resistive fault coverage limited by Zone 1
•    Dependent on VT signals
•    No intertripping signal from weak end in feed I open terminal tripping
•    No weak end in feed I open terminal tripping
•    No detection of series faults
•    Many designs can be directionally unstable for series compensated lines
•    Zone 1 reach problems for series compensated lines
•    Lack of discrimination for faults between circuits of different voltage levels

5.5.2.4 PermIssIve Overreach DIstance ProtectIon
Attributes
•    Communication independent fast tripping at both ends for about 60% of the
     protected line
•    Accelerated tripping at one end for faults in about 40% of the protected line
•    Offers remote back-up protection
•    Offers substation back-up (Offset Z3 or Z4)
•    Can be phase selective
•    Suitable for large in-zone loads
•    Suitable for transformer feeders
•    Suitable for composite circuits (lines/cables)
•    Suitable for multi-terminal lines where all faults can be seen by Zone-2 from all
     terminals (no out feed)
•    Open terminal signal echo logic possible
•    Suitable for series compensated lines with special designs provide directional
     discrimination
Limitations
•    Delayed tripping at ends of the line (for about 40% of protected line) in case of
     communication failure
•    Resistive fault coverage limited by Zone 2
•    Dependent on VT signals

42                      Manual on Reliable Fault Clearance and Back-Up Protection of
                                   EHVand UHV Transmission Networks

•        No permissive trip signal from weak end in feed / open terminal
•        No weak end in feed / open terminal tripping
•        No detection of series faults
•        Many designs can be directionally unstable for series compensated lines
•        Zone 1 reach problems for series compensated lines
•        Lack of discrimination for faults between circuits of different voltage levels

5.5.2.5 Permissive overreach distance protection with weak in feed logic

     Zone-R
                                                                                         Zone-2

    STRONG                              Zone-1                                                    WEAK
    SOURCE                                                                                        SOURCE

                                                                               I
                                                                               I
                              I                   DUPLEX                       :
                              I             SIGNALLING LINK                    I

                            ~--------------------------~
                            ~--------------------------~

                                                      Zone-1
              Zone-2

                                                                                                  Izone-RI
     Additional Open-Terminal Echo Logic                            Additional Open-Terminal Echo Logic

                                  tW   = Weak Infeed TRip Discrimination Timer
                                  tE   = Echo Duralion Control Timer

                       Fig. 5.2 Permissive overreach distance protection with weak infeed logic

                              Chapter 5 : Unes and Cables                             43

Attributes

•    Communication independent fast tripping at both ends for about 60% of the
     protected line
•    Accelerated tripping at one end for faults in about 40% of the protected line
•    Offers remote back-up protection
•    Offers substation back-up (Offset Z3 or Z4)
•    Can be phase selective
•    Suitable for large in-zone loads
•    Suitable for transformer feeders
•    Suitable for composite circuits (lines/cables)
•    Suitable for multi-terminal lines where all faults can be seen by Zone-2 from all
     terminals (no out feed)
•    Open terminal signal echo logic possible
•    Suitable for series compensated lines with special designs provide directional
     discrimination
Limitations
•    Delayed tripping at one end for about 40% of protected line in case of
     communication failure
•    Resistive fault coverage limited by Zone 2
•    Dependent on VT signals
•    No detection of series faults
•    Many designs can be directionally unstable for series compensated lines
•    Zone 1 reach problems for series compensated lines
•    Lack of discrimination for faults between circuits of different voltage levels

5.5.2.6 Blocking Overreach Distance Protection
Attributes
•    Communication independent fast tripping at both ends for about 60% of the
     protected line
•    Communication independent tripping with small delay at one end for faults in
     about 40% of the protected line
•    Offers remote back-up protection

44                     Manual on Reliable Fault Clearance and Back-Up Protection of
                                  EHVand UHV Transmission Networks

•     Offers substation back-up (Offset Z3 or Z4)
•     Can be phase selective
•     Suitable for large in-zone loads
•     Suitable for transformer feeders
•     Suitable for composite circuits (lines/cables)
•     Suitable for multi-terminal lines where there is no out feed for an internal fault
•     No degradation of performance at other terminals with weak-infeed at one
      terminal
•     Dependable scheme for use with PLC (where in-zone fault attenuates PLC)
•     Suitable for series compensated lines with special designs provide directional
      discrimination

     Zone-R
                                                                                  Zon9-2

                                      Zone-l

                             I
                             I
                             :          SIMPLEX OR DUPLEX                  I
                                          SIGNALLING LINK
                           L.::J-------------------------------t.::J
                             I                                             I

                           ~---------------------------~
                                                  Zone-l
              Zone-2

                                                                                           Zone-R

                         Fig. 5.3 Blocking overreach distance protection

Limitations
•     Resistive fault coverage limited by Zone 2

                               Chapter 5 : Unes and Cables                            45

•    Dependent on VT signals
•    Loss of external fault security with undetected communication failure
•    No tripping at weak in feed terminal
•    No detection of series faults
•    Many designs can be directionally unstable for series compensated lines
•    Zone 1 reach problems for series compensated lines
•    Lack of discrimination for faults between circuits of different voltage levels

5.5.3 Phase Comparison Protection
5.5.3.1 Modulated Power Line Carrier Communication
Attributes
•    Fast tripping for 100% of line
•    Communication independent tripping
•    Suitable for transformer feeders
•    Suitable for composite circuits (lines/cables)
•    Tripping with one weak! open terminal
•    Tripping not affected by PLC attenuation
•    Moderate resistive fault coverage
•    Not dependent on VT signal
•    Often suitable for series compensated lines with spark-gap capacitors and no
     internal fault current inversion
•    Can discriminate for faults between conductors at different voltage levels
Limitations
•    Loss of external fault security with undetected communication failure
•    No remote back-up protection
•    No tripping at weak in feed terminal
•    Needs additional units for phase selection
•    Not usually suitable for multi terminal lines
•    Not suitable for transformer feeders
•    No detection of series faults

46               Manual on Reliable FauN elBa"""", and Back-Up _    of
                            EHVand UHV Tnmsmission N9Iwot1rs

•    Not suitable for series compensated lines with current reversal or large
     deviations in internal fault current angle at one relay terminal for resistive
     faults

5_5_4 Current Differential Protection
5_5_4_1 Digital Communication
Attributes
•    Fully discriminative without time delays
•    Independent of VT signals
•    Moderate to high resistive fault coverage
•    Can be inherently phase- selective
•    No problems with parallel circuits
•    Suitable for composite circuits
•    Tripping at all ends for internal faults without in feed from all ends
•    Possible application to multi-terminal lines (some designs)
•    No problems with series compensation
•    No problems with power swings
•    Variety of communications media possible
•    Sophisticated supervision of communication links included
•    Communication error checking for security
•    Discriminatively detects faults between conductors at different voltage levels
•    Operational during single pole AIR
•    Single phase tripping possible for simultaneous faults on parallel lines
Limitations
•    Dependent on communication
•    Does not inherently offer remote back-up protection
•    Commissioning difficulties for long lines
•    Sensitivity varies with load
•    Shunt capacitance may limit sensitivity
•    Unstable with large in zone loads
•    No detection of series faults (Broken conductors etc.)

                                  Chapter 5 : Unes and Cables                     47

5.5.4.2 Pilot Wire Communication
Attributes
•    Fully discriminative without time delays
•    Independent of VT signals
•    Moderate to high resistive fault coverage
•    No problems with parallel circuits
•    Suitable for composite circuits
•    Tripping at all ends for internal faults (some designs)
•    No problems with series compensation
•    No problems with power swings
•    Discriminatively detects faults between conductors at different voltage levels
•    Supervision of pilots is possible (For security and dependability)
•    Operational during single pole AIR
•    Relatively low cost relays
•    Single phase tripping possible for simultaneous faults on parallel lines
Limitations
•    No remote back·up protection
•    Not phase selective
•    In feed terminal trip only
•    Protection dependent on healthy pilots
•    Requires metallic pilots
•    Commissioning difficulties for long lines
•    Limited to relatively short lines
•    Insulation required for induced voltages in parallel and differences between
     substation ground potentials
•    Sensitivity varies with load (Biased schemes)
•    Shunt capacitance may limit sensitivity
•    Unstable with large in zone loads
•    No detection of series faults (Broken jumpers etc)

48               Manual on Reliable FauN elBa"""", and Back-Up _   of
                            EHVand UHV Tnmsmission N9Iwot1rs

5_5_5 Directional Protection
5_5_5_1 Directional Comparison Protection (Permissive)
Attributes
•    Variety of communication media possible
•    Fully discriminative with short time delays
•    Suitable for long lines
•    Can be phase selective (by design)
•    Moderate-high resistive fault coverage
•    Weak-infeed / open-terminal logic possible
•    Possible application to multi-terminal lines
•    Protection of parallel circuits
•    Suitable for composite circuits
•    Possible detection of series faults
•    Some special designs are suitable for series compensated lines
•    Discriminative detection of faults between conductors at different voltage
     levels
Limitations
•    No remote back-up protection
•    Protection dependent on communication
•    Unstable with large in zone loads
•    Some standard designs e.g., DEF are not universally suitable for series
     compensated lines
•    Pick up for external faults with no reach control elements
•    Dependent on VT signals
•    Directional ground fault protection must be inhibited during single pole dead
     times
5.5.5_2 Directional Comparison Protection (Blocking)
Attributes
•    Variety of communication media possible
•    Fully discriminative with short time delays
•    Communications independent tripping

                                Chapter 5 : Unes and Cables                          49

•     Suitable for long lines
•     Can be inherently phase selective (by design)
•     Moderate-high resistive fault coverage
•     Possible application to multi-terminal lines
•     Protection of parallel circuits
•     Suitable for composite circuits
•     Possible application to multi-terminal lines
•     Possible detection of series faults
•     Some special designs are suitable for series compensated lines
•     Discriminative detection of faults between conductors at different voltage
      levels
Limitations
•     Security is dependent on communication
•     No remote back-up protection
•     Unstable with large in zone loads
•     Some standard designs e.g., DEF are not universally suitable for series
      compensated lines
•     Pick up for external faults with no reach control elements
•     Dependent on VT signals
•     Directional ground fault protection must be inhibited during single pole dead
      times

5.5.6 cable Circuit Considerations

The attributes and limitations of individual protection schemes described above are
mainly made with respect to overhead or hybrid transmission circuits. For pure cable
circuits, which are generally relatively short in length, the most common and
favoured form of protection is current differential protection. Here again, it should be
preferably current differential protection using digital communication and not pilot
wires as the experience with the latter has not been satisfactory, especially where
pilots are laid in the same trench in which power cables are laid. This is often the
case in city areas where distances are more than a kilometer.

      Remote back-up protection can be provided by time-delayed phase over
current and ground over current protection or by overreaching time-delayed zones of
distance protection.

50                 Manual on Reliable FauN elBa"""", and Back-Up _   of
                              EHVand UHV Tnmsmission N9Iwot1rs

       The relatively low impedance of cables per unit length, together with the
relatively short length for a cable circuit has traditionally precluded the application of
distance protection in view of the low impedance setting which would be required for
under reaching zone of protection. However, distance relays have been applied in
blocking overreaching or permissive overreach signaling channel-aided schemes,
without under reaching zones.

       With the advent of modern numerical distance relays, with lower impedance
setting ranges, better accuracy at low impedance settings and with the necessary
range and accuracy of neutral impedance compensation available it is now more
feasible to apply under reaching distance protection schemes to cable circuits as
short as 2 km in length.

      The distance relay when applied should preferably be as Main-2 protection.

5.6   TRANSMISSION CIRCUIT BACK-UP PROTECTION
This section examines various forms of circuit back-up protection.

5.6.1 Distance Protection as Main and Back-up Protection
Multi-zone distance protection is a popular form of main and back-up protection for
HV and EHV transmission circuits. Zone-1 distance protection elements will offer
main protection for a stand-alone distance protection scheme, but they cannot cover
the entire length of the protected circuit.

       To achieve fast clearance of faults at any location within a transmission circuit,
it is usual to use distance protection relays with protection signaling equipment.
Where distance teleprotection is applied, the Zone-1 distance protection provides
high speed tripping for a limited reach.

      The Zone-1 distance elements must be set to under reach a protected circuit
to ensure external fault security. It may be necessary to increase the degree of
under reach to deal with a parallel transmission circuit being switched out and
grounded at both terminals. For multi-terminal lines, the Zone-1 coverage will be
further reduced as a result of the apparent impedance effects.

5.6.2 Zone-l Distance as Circuit-Local Back-up
Zone1 instantaneous distance elements offer circuit-local back-up protection for
nearby faults, but not for the entire transmission circuit from both terminals.

                               Chapter 5 : Unes and Cables                         51

5.6.3 Zone-2 Distance as Circuit-Local Back-up
5.6.3.1 Zone-2 Reach Setting Criteria
Zone-2 distance protection can offer time·delayed circuit-local back·up protection for
the entire protected circuit. To achieve this, Zone·2 distance elements must be set
according to the following criteria.

•     Zone·2 should overreach all terminals of the protected circuit by an acceptable
      margin (typically 20% of highest impedance seen) for all fault conditions and
      for all intended modes of system operation.

•     As far as possible, Zone·2 reach should be less than Zone-1 coverage of all
      adjacent lines, to minimize the required Zone·2 time delay setting.

5.6.3.2 Zone-2 Time Setting Criteria
Since Zone-2 distance protection must be set to overreach the circuit it is intended
to protect, it will also be responsive to faults within adjacent power system circuit.
For this reason the time delay for Zone-2 back-up protection must be set to
coordinate with clearance of adjacent circuit faults, within reach, by the intended
main protection or by breaker fail protection.

     The following formula would be the basis for determining the minimum
acceptable Zone·2 time setting:

      t,2 > tMA +tCB +t,2"",' +t,
where:
Iz2   = Required Zone-2 time delay
tMA   = Operating time of slowest adjacent circuit main protection or Circuit Local
        back-up for faults within Zone-2 reach
Ie. = Associated adjacent circuit breaker clearance time
Iz2reset = Resetting time of Zone-2 impedance element with load current Present
Is       = Safety margin for tolerance (e.g. 100 ms)

5.6.3.3 Consideration of Zero Sequence Mutual Coupling for Parallel Circuits
It is necessary to consider the under reaching effects of zero sequence mutual
coupling on ground fault impedance measurement when setting the reach of Zone·2
distance protection to meet the primary reach criterion for parallel circuits. Where
common impedance settings exist for phase and ground fault impedance elements,
or where independent residual compensation settings are not available for each
zone of protection the phase fault Zone·2 reach will unavoidably be extended in
order to satisfy ground fault reach requirements. This can create Zone-2 back·up co-

52                   Manual on Reliable FauN elBa"""", and Back-Up _   of
                                EHVand UHV Tnmsmission N9Iwot1rs

ordination difficulties, particularly where adjacent sections or transmission circuit are
of unequal length.

     Modern numerical distance relays generally have feature of individual zero
sequence compensation factor for each zone of ground fault element.

     In these protections it is generally possible to compensate influence of zero
sequence mutual coupling in following ways.
•     By using possibility of different values of earth return compensation factor K
      for different zones within the same group of setting parameters.
•     By using different groups of setting parameters for different operating
      conditions of protected double circuit line.

      Where feasible these methods shall be used. More details pertaining to theory
behind this can be found in the document produced by CIGRE WG 34.04 titled
"Application guide on protection of complex transmission network configurations".

       In CBIP Publication No 274 titled "Protection of Generators, Generator
Transformers and 220 kV and 400 kV Networks" some recommendations for the
settings to be adopted for distance relays in parallel transmission circuits are made.
Where the distance relays have common zero sequence compensation factor for all
the zones or it is decided to use common zero sequence compensation factor, these
recommendations may be followed.

      The following explains basis for arriving at these recommendations:

•     Zone 1 of distance relay should not overreach the protected line under all
      conditions. In case of a double circuit line under conditions when parallel line
      is disconnected and grounded the relay tends to overreach for single line to
      ground faults. This can be of the order of 20% with conventional Ko setting.
      Based on this the Zone 1 setting will have to be limited to 60-65%.

•     Zone 2 of distance relay should not under reach the protected line under all
      conditions. In case of double circuit line when both lines are in service the
      relay can under reach for a single line to ground faults by as much as 30-35%
      with conventional Ko setting.

       In the grid there are mix of electromechanical, static and numerical relays.
Even though the numerical relays have features to take care of the above effects, by
using different values of Ko for different zones or by using different groups of
settings parameters, to keep uniformity in approach following recommendations
were made:
•     Zone 1 to be set to cover 80-85% of protected line length

                                       Chapter 5 : Lines and Cables                                       53

•          Zone 2 to be set to cover minimum 120% of principle section. However in case
           of double circuit lines 150% coverage must be provided to take care of under
           reaching due to mutual coupling effect but care is to be taken that it does not
           reach in to next lower voltage level.
•          Zone 3 for 400 kV lines is to be set to cover 120% of principle section plus
           adjacent longest section subject to reach restriction so that it does not reach in
           to next lower voltage level. For 220 kV lines, Zone 3 reach may be provided to
           cover adjacent longest section if there is no provision of LBB or all protections
           are connected to single DC source at remote end substation.
•          Resistive reach should be set to give maximum coverage subject to check of
           possibility against load point encroachment considering maximum expected
           voltage and maximum load. Also attention has to be given to any limitations
           indicated by manufacturer in respect of resistive setting vis-a-vis reactance
           setting.

5.6.3.4 Zone-2 Application with a short Adjacent Circuit Section

                                                                                           m-e-3F
                 r:::::::::::::l------~-i---------T"""I -::=-1-----2-1
                                                                                                     1 -----.

      Zone'3R                                                -I              1 ___ 1
                                                                         --+,-,
                                                                                            Zale-2
                 :            Zale-1                Zale-1                   Zale-1

                      B-                            B-                 B-
                                               I                  I

                        I                              I                 I

          Time

---   I

                     Fig. 5.4 Application of Zone-2 back-up with unequal circuit lengths

     Unequal lengths of transmission circuit can make it difficult to meet the Zone-2
secondary reach setting criterion. Where the secondary criterion has to be
abandoned in order to meet the primary criterion, it will be necessary to co-ordinate
Zone-2 with longer time delay. The time tMA in equation must be the adjacent circuit
Zone-2 protection operating time.

54                Manual on Reliable FauN elBa"""", and Back-Up _   of
                             EHVand UHV Tnmsmission N9Iwot1rs

5_6_3_5 Application to Multi-terminal Circuits
For multi-terminal circuits, the primary Zone-2 setting criterion must be met with
allowance for the highest apparent impedance seen for a fault at any remote circuit
terminal.

      In such an application, the Zone-2 reach setting may reach very high
percentage of the circuit impedance between the closest terminals. The reach may
need to be further enhanced to address under reach for ground faults when
protecting parallel multi-terminal circuits.

5.6.3_6 Zone-2 Load Impedance Encroachment
One problem with mho impedance elements is that the fault resistance coverage
varies with the forward reach setting. When applying Zone-l elements to short lines,
fault resistance coverage may be insufficient. It can also be disadvantage for Zone--
2 elements to be set with unusually high forward reach setting in relation to the
minimum load impedance. It may be possible for the minimum load impedance to
encroach upon the Zone-2 operating region.

5.6.3_7 Adaptive Zone-2 Back-up Protection for Tee-off Transformer Feeders
In teed substation application, permissive under reach distance protection would be
ineffective if the feeder is energized from one terminal only. Delayed Zone-2 back-up
protection could be adapted to become the main protection at the energized
terminal. One of the practices is to automatically bypass the Zone-2 delay of a
distance relay when the remote terminal of such circuit is open.

5.6.4 Distance Zone-3 Remote Back-up
Where Zone-3 distance protection is applied, it is usually set to provide remote back-
up protection for adjacent sections of a transmission circuit. Zone-3 impedance
elements may have independently adjustable forward and reverse reach setting (i.e.
semi directional). In most applications, it is forward reach, which provides remote
back-up protection. When transmission circuits are provided with duplicate main
protection, there may be a case for not applying Zone-3 remote back-up protection
at all. As for example in case of long 400 kV lines it may be desirable either to
reduce the reach or to block 3 0d zone of distance relay for reasons of security.

5.6.4_1 Forward Reach Setting Criteria
Zone-3 distance protection can offer time-delayed remote back-up protection for an
adjacent transmission circuit. To achieve this, Zone-3 distance elements must be set
according to the following criteria where possible.

                               Chapter 5 : Unes and Cables                          55

•     Zone-3 should overreach the remote terminal of the longest adjacent line by
      an acceptable margin (typically 20% of highest impedance seen) for all fault
      conditions and in feed conditions associated with all intended modes of
      system operation.

•     Zone-3 reach should be less than the Zone-2 protection coverage of the
      shortest adjacent transmission circuit and it should not see through power
      transformers into distribution systems, in order to minimize the required zone-
      3 time delay setting.

5.6.4_2 Zone-3 Time Setting Criteria
Since Zone-3 distance protection must be set to overreach adjacent circuits, it will
be responsive to faults that should be cleared by adjacent circuit-local back-up
protection in the event of any main protection failure. For this reason the time delay
for Zone-3 protection must be set to co-ordinate with clearance of faults by adjacent
circuit-local back-up protection. This is commonly Zone-2 distance protection. For
other circuits, it may be time delayed over current protection.

     The following formula would be the basis for determining the minimum
acceptable Zone-3 time setting:

where:
         tzs      = Required Zone-3 time delay
         tMA      = Operating time of slowest adjacent circuit local back-up protection
         teB      = Associated adjacent circuit breaker clearance time
         tzs..... = Resetting time of Zone-3 impedance element with load current
                    present
         ts       = Safety margin for tolerance (e.g. 100ms)
5.6.4_3 Consideration of Zero Sequence Mutual Coupling for Parallel Circuits
As for Zone-2 protection for Zone-3 protection too, the under reaching effect of zero
sequence mutual coupling for remote ground faults must also be considered in
relation to the primary reach setting criterion. Such consideration is quite complex,
since there may well be differences in the levels of mutual coupling for the protected
circuit and any number of adjacent circuits. In addition, some circuit sections may be
multi-circuit while other sections may not be.

56                Manual on Reliable FauN elBa"""", and Back-Up _   of
                             EHVand UHV Tnmsmission N9Iwot1rs

5_6_4_4 ConsIderatIon of IntervenIng Fault Current In Feeds
The under reaching effect of fault current in feed from an additional terminal of a
transmission circuit has been highlighted in section 5.6.3.5. Similar effects are
encountered in relation to adjacent circuit impedance, when applying Zone-3 remote
back-up protection. These under-reaching effects are particularly difficult to address,
since they are variable according to the type of fault. Ground faults can invoke
additional zero sequence current in feed from transformers with grounded star-
connected primary windings and other delta-connected windings.

5.6.4_5 Zone-3 Load Impedance Encroachment
With the extended Zone-3 reach settings, that may be required to address the many
under reaching factors already considered, load impedance encroachment is a
significant risk when Mho-type impedance elements are applied to long lines of an
interconnected power system. Not only must the minimum load impedance under
expected modes of system operation be considered in risk assessment, but also the
minimum impedance that might be sustained for seconds or minutes during
abnormal or emergency system situations. Failure to do so could jeopardize power
system security.

       Ideal solution to tackle load encroachment may be based on use of blinders
in case of Mho type of elements, by specially shaped impedance elements or by use
of polygon type impedance elements. Even with shaped characteristics in case of
long 400 kV transmission lines it may be desirable to limit the reach of Zone-3 for
reasons of security. It is felt that in such cases, if the adjacent station has bus bar
protection and breaker failure protection, Zone-3 can be dispensed with.

      For example ESKOM (South Africa) have a practice of not using third zone
impedance protection in long line applications due to the reduced security of very
long reaches which may encroach on emergency load conditions. Their concept is
enhanced local breaker back-up, i.e., extensive duplicated breaker failure protection,
obviates the need for remote (third zone) back-up. It may be noted here that they
provide duplicated breaker failure protection.

5.6.5 Distance Zone-4 Substation-local Back-up
Zone-3 distance protection is usually targeted to provide only remote back-up
protection. In such a case, the distance relay may be provided with an additional
zone of reverse-looking protection (e.g. Zone-4) to offer substation-local back-up
protection. The criterion for setting Zone-4 reverse reach would be as under.

•     The Zone-4 reverse reach must adequately cover expected levels of apparent
      bus bar fault resistance, when allowing for multiple in feeds from other circuits.

                                Chapter 5 : Unes and Cables                           57

       It is difficult to precisely apply the above criterion and in such cases the
practice is to set Zone-4 reverse reach to something like 25% of the associated
Zone-1 forward reach.

       With a reverse reach setting of less than the Zone-1 reach of distance
protection for the shortest line connected to the local bus bar, the Zone-4 time delay
would only need to co-ordinate with bus bar main protection fault clearance and with
Zone-1 fault clearance for lines out of the same substation. This would be according
to the Zone-2 time setting guidelines given in section 5.6.3.2 above.

       Sometimes when separate reverse looking element is not available the above
is achieved by offset reach of Zone-3 of distance relay. The resistive fault coverage
of offset-mho Zone-3 elements will, however, depend on the forward and reverse
reach setting. The Zone-3 reverse reach, in conjunction with the forward reach, must
be set to adequately cover expected apparent fault resistance, while allowing for
multiple feeds from other circuits. The time delay however will be that of Zone-3.

5.6.6 Use of System Studies to Analyse Behaviour of Distance Relays During
      System Disturbances
      Often during system disturbance conditions, due to tripping of one or more
trunk lines, some lines get overloaded and the system voltage falls. During such
conditions the back-up distance elements may become susceptible to operation due
to encroachment of impedance locus in to the distance relay characteristic.

      While the ohmic characteristic of a distance relay is independent of voltage,
the load is not generally a constant impedance. The apparent impedance presented
to a distance relay, as the load voltage varies, will depend on the voltage
characteristic of the load. If the low voltage situation resulted from the loss of one or
more transmission lines or generating units, there may be a substantial change in
the real and reactive power flow through the line in question. The combination of low
voltage and worsened phase angle may cause a long set relay to operate
undesirably either on steady state basis, or in response to recoverable swings
related to the initiating event.

       It is desirable that system studies are conducted using computer-aided tools
to assess the security of protection by finding out trajectory of impedance in various
zones of distance relay under abnormal or emergency system condition on case-to-
case basis. Since validity of such studies depend on the validity of data, if practice of
conducting such studies exist, the quality of data improves over a period and the
results then can be trusted when one really looks for answers regarding settings to
be adopted.

58                Manual on Reliable FauN elBa"""", and Back-Up _   of
                             EHVand UHV Tnmsmission N9Iwot1rs

5_6_7 Phase Over Current I Ground Over Current Protections for Local and
      Remote Back-up
Phase over current protection both non-directional and directional types are applied
when single main protection is applied as transmission circuit back-up protection.
The ground over current protection, both non directional and directional types are
applied as a circuit back-up protection when single main protection is applied and
also as a supplement to distance protection wherever distance relays are used.

     The phase over current protection offers both circuit local back-up protection
and remote back-up protection for multi phase faults. They also offer protection for
many faults involving ground if fault current is high enough to allow relay operation.

      To cater to low current ground faults as a result of high ground fault resistance
the ground over current protections are applied. They act as a supplement to phase
over current protection. They might also be applied, as main protection for high
resistance faults where main protection does not offer required coverage.

5.6.7_1 Non-directiona' Phase Over Current Protection
For radial lines normally non-directional over current protection is used as back-up
protection. Such protections offer both circuit local back-up and remote back-up for
shunt faults. (The implication for avoiding the use of the conventional IDMT relays
for over current back-up protection or more secure and simple definite time OIC
relays may be kept in view)

      Phase over current relays should be set according to following criteria:
•     The protection must not operate for highest load current during both normal
      and abnormal power system operation.
•     The protection must operate for multiphase faults on the entire circuit under
      minimum plant conditions i.e. lowest fault current.
The operating time must be set according to the following criteria:
•     The protection should not operate before the main protection of the protected
      circuit
•     The protection must not operate before the circuit local back-up protection
      clears a fault in an adjacent circuit.

5.6.7_2 Directiona' Phase Over current Protection
It is difficult to co-ordinate, non-directional (inverse-time) over current protection on
non-radial transmission circuits, if the power system is not sufficiently interconnected
to create a significant difference between faulted circuit currents and in feed circuit
currents. The application of directional phase over current protection eases such co-
ordination difficulties.

                                Chapter 5 : Unes and Cables                           59

      Directional protections may also be applied for:
•     Receiving terminals of radial parallel circuits
•     Where fault current in one direction is low in comparison to load current in the
      other direction.

5.6.7.3 Non-directional Ground Over Current Protection
For radial lines normally this protection is applied as a supplement to main
protection when ground fault currents may be lower than the threshold of phase over
current protection. It might also be applied as main protection for high resistance
faults.

      The ground over current threshold should be set to ensure detection of all
ground faults, but above any continuous residual current under normal system
operation. Continuous residual current may arise because of:
•     Unbalanced series impedances of untransposed transmission circuits
•     Unbalanced shunt capacitance of transmission circuits.
•     Third harmonic current circulation.

5.6.7.4 Directional Ground Over Current Protection
The purpose of this protection is similar to that described for non·directional
protection. Directional ground protection is also applied as main protection for high
resistance faults wherever it is felt that Main protection does not cover the high
resistance faults adequately.

     Various types of directional elements may be employed to control operation of
ground over current (zero sequence over current) protection response. The most
common approach is

•     Phase angle difference between Zero sequence voltage and current

      Since the relaying signals can easily be derived by summing phase current
signals and by summing phase voltage signals from a suitable voltage transformer.

       However this method is not suitable for some applications where transmission
lines run partially in parallel to different substations. In such cases following type of
directional control is recommended to be used for the directional earth fault relay.

•     Relative phase of negative sequence voltage and current

60                Manual on Reliable FauN elBa"""", and Back-Up _   of
                             EHVand UHV Tnmsmission N9Iwot1rs

5_7   RECOMMENDATIONS FOR PROVISION OF MAIN 1, MAIN 2 AND BACK-
      UP PROTECTIONS
Transmission line protection is the most complex of all the protections in terms of the
challenges it poses. In the above paragraphs many of these aspects connected with
line and cable protection and some recommendations have been brought out and
these should be considered. Few of these are brought out below.

•     Section 5.5 gives details of main attributes and limitations of various main
      protections. When applying any of the main protections these should be fully
      examined and understood.
•     The decision to provide Main-2 protection and effective back-up protection
      should not be merely based on voltage level but on how important the circuit
      is. The costs of reduced supply capacity or total loss of supply must be
      considered in relation to the cost of providing effective protective system.
•     Directional ground protection should be applied as main protection for high
      resistance faults wherever it is felt that Main protections applied do not cover
      the high resistance faults adequately.
•     When unit protections are used, Phase-segregated unit protection based on
      current measurement is the best option, when it is economically and
      technically feasible.
•     Cables do not withstand fault currents for long periods of time. Unit protection
      should be used as main protection and distance protection shall be used as
      Main-2.
•     For details concerning protection of complex transmission lines reference may
      be made to CIGRE WG 34.04 report titled "Application guide on protection of
      complex transmission network configurations'. Use of correct line parameters
      is important for proper setting of protective relays. Calculated values of
      overhead line electrical parameters ought be verified by field-testing and this
      information then be used for relay setting.
•     Setting guidelines are given for double circuit lines. These shall be followed.
      Detailed explanations of these can be found in the CIGRE document
      mentioned above.
•     Section 5.6 gives how distance relay is applied as circuit local back-up,
      remote back-up, substation local back-up. Guidelines given here for setting
      the relays shall be followed. This section also gives some guidelines for
      setting of over current and ground over current relays. These too should be
      considered. It is desirable that system studies are conducted using computer-
      aided tools to assess the security of protection by finding out trajectory of
      impedance in various zones of distance relay under abnormal or emergency
      system condition on case-to-case basis. When transmission circuits are
      provided with duplicate main protection there may be a case for not applying

                                Chapter 5 : Unes and Cables                            61

      Zone-3 remote back-up protection for reasons of security. Such cases may
      emerge from such studies.
•     The potential loss of system generation or the potential challenges to nuclear
      plant safety systems may be factors which will dictate the longest acceptable
      clearance times for transmission circuit faults in the vicinity of a power station.
      This should be kept in mind while designing protection system close to these
      locations.

       Provision of independent Main-1 and Main-2 protection is important to ensure
clearance of all faults in the shortest possible time. As per the current practice this is
followed for all lines at 765 kV, 400 kV level and in some cases for lines at 220 kV
level. No change is proposed in this practice. Reference may be made to CBIP
Manual No. 274 "Protection of Generators, Transformers and 220 kV and 400 kV
Networks·, which gives details of current practices being followed.

       With growing interconnections fast fault clearance in 220 kV lines is becoming
important to avoid grid disturbances. Therefore it is recommended that for all 220 kV
lines too Main 1 and Main 2 protections be provided.

      For 132 kV lines it is felt that provision of one Main protection and directional
over current and earth fault protection as back-up protection is adequate. However if
in any given part of the 132kV network, failure of fault clearance by primary
protection is going to create wide spread disturbance and consequences of such
disturbances are too costly, provision of Main 2 protection should be considered
here too.

       If only one main protection is used, the back-up protection should be provided
in a separate hard ware unit.

      Distance relays have inherent features for providing back-up protection. When
a distance protection is provided as Main protection the Zone 2 element of the
distance relay provides circuit local back-up, the Zone-3 element provides remote
back-up and reverse reach element of Zone 4 provides substation local back-up.

        In case a line differentiaVphase comparison/directional comparison protection
is used they do not have inherent features to provide back-up protection. Therefore,
it is recommended that they should preferably be provided with additional elements
that can provide back-up protection. Usually these features are achieved by
supplementing the unit protections with additional impedance elements.

      It is felt that for transmission overhead line a non segregated type phase
comparison protection may not provide the correct practical solution to protection
problem due to several technical reasons. Though segregated type phase
comparison protection overcomes these limitations, the overall cost may be too high.

## Chapter 6: Power Transformers

POWER TRANSFORMERS
      The most widely used transformer at high voltage level is the Interconnecting
Auto-transformer without tertiary winding and the Interconnecting Auto-transformer
with a tertiary winding. Two and three winding transformers such as 400 kV/33 kV,
220 kV/33 kV and 132 kV/33 or 11 kV are also used quite extensively at the
transmission level. Transformer protection practices encompass a wide variety of
protection schemes and philosophies.

6.1   TRANSFORMER DESIGN
The magnetic circuit plays a key role in transformer protection because it influences
the excitation current. In steady state, the excitation current contains odd harmonics.
During energisation or faults, the excitation current may become unbalanced and
contains large amounts of even harmonics.

       The transformer oil is circulated in some manner to remove the heat from the
windings. The oil flows from the bottom of the tank, through the windings and to the
top of the tank. This top oil temperature is usually measured and monitored. In
addition, the winding temperature is monitored to limit insulation deterioration. The
highest temperature occurs just inside the insulation on the conductor. The point
with the highest temperature is referred to as the hot spot. Another heating source is
the eddy current losses in the core. The resistive losses in the winding conductors
and excitation current losses in the magnetic cores are two major sources of steady
state heating in the transformer. Over-excitation results in excessive excitation
currents, eddy current losses, and core heating.

       Fault currents quickly increase the winding temperature. Transformers must
withstand fault currents for a given time. Axial and radial forces are generated on the
windings due to these currents, which may damage the insulation. The first current
peak of fault current causes the maximum forces, which determines the withstand
limit.

6.2   TYPICAL TRANSFORMER ARRANGEMENTS
Transformer arrangements are usually independent of the type of transformer being
used. Mostly these are decided by substation cost and operating reliability needs.
Arrangements are more a product of substation costs and system operating
reliability needs. Figure 1 covers some of the typical transformer arrangements.
•     Figure 6.1 A is the simplest with dedicated high and low side breakers.
•     Figure 6.1 B adds a breaker and a half or a ring bus configuration to allow
      breaker maintenance and switching flexibility on high voltage side.

64                    Manual on Reliable FauN C/eatanca and _-Up Protaction of
                                 EHV and UHV Transmission Networl<s

•       Figure 6.1 adds a breaker and a half or a ring bus configuration to allow
        breaker maintenance and switching flexibility on high voltage as well as low
        voltage side.

                      A                 B                     c
              Fig. 8.1 Typical transformer arrangements

6.3     FAILURE RATES OF POWER TRANSFORMER
The failure rates of power transformers range from 1% to 4% per year for 132 kV to
400 kV class and reported to be around 6 % for 765 kV systems. The number of
through faults may influence the failure rate.

Table 1 given below from IEEE can be taken as typical of transformer failure modes.

Table 1 Transmission power transformer, IEEE 1975-1982
      S.NO.              Mode                                         Number     %
        1                Windina Failures                               615      51
        2                Tap Chanasr Failures                           231      19
        3                Bushing Failures                               114      09
        4                Terminal Board Failures                         71      06
        5                Core Failures                                   24      02
        6                Miscellaneous Failure                           72      13

       Winding failures still represent the major exposure to transformer failure with
tap changers being a distant second. Two characteristics of transformers that cause
problems for protection schemes are low magnitude turn-to-turn faults and high
magnitude magnetizing inrush current during energizing. Some internal faults can
result in less than 10% of a transformer rated current. On the other hand maximum
fault current can flow for a high side transformer bushing failure.

                                Chapter 6 : Pawsr Transfonnsrs                    65

6.4   TRANSFORMER PROTECTION REQUIREMENTS
The transmission transformer is a major component in the bulk power system and is
normally held to a single contingency failure requirement. Based on the types of
failures and the basic design of the transformer and the requirements of the power
system, the protective relaying schemes must meet the following main requirements:

•     Maintain transient stability of the power system.
•     Prevent unwanted operation by load currents or by inrush currents or OLTC
      operation
•     Maintain required quality of power
•     Provide for maintenance of protective equipment with primary equipment
      energized by providing two groups of protections
      The protection system must satisfy the following requirements specific to the
transmission transformer:
•     Protect for internal tank faults to ground or to altemate phases.
•     Protect for external tank faults to ground or to alternate phases.
•     Protect for internal partial winding or turn-to-turn faults.
•     Limit through fault magnitude and duration within transformer mechanical and
      thermal ratings.
•     Limit top oil temperature to maximum temperature limit
•     Limit hot spot winding temperature to maximum temperature limit
•     Prevent rupture of transformer tank during intemal fault
•     Provide for failure of a switching device
•     Limit ove~oad as per thermal capability of the transformer
•     Provide for tertiary winding protections over voltages caused due to
      transferred lightning surges or switching surges from high voltage sides
•     Provide protection of winding insulation by suitably dimensioned and
      monitored surge arresters
•     Provide for over-excitation of transformer core (limited to Generator Step-up
      transformer: Refer CIGRE WG Report on Overfluxing)

      Most transmission transformers are located in critical areas of the power
system where either utility voltage stability or transient stability is a problem.
Providing high-speed clearing to meet generator voltage and stability limits is
essential.

66               Manual on Reliable FauN C/eatanca and _-Up Protaction of
                           EHV and UHV Transmission Networl<s

        One of the key problems in security of a transmission transformer is tripping
during a through fault current flow. In many cases, this means that the faulted
element (usually a transmission line) will be properly tripped by the protection
provided for it, failing which the back-up protection of the transmission transformer
will trip the transformer. This common mode failure where both line and transformer
gets disconnected, can be disastrous to a single contingency designed power
system. In many systems the single contingency limit only exists during the peak
load of the power system, which greatly reduces the possibility of cascading failures.
It does identify a serious potential problem if through fault trips are allowed to
happen.
      Turn-to-turn faults challenge the dependability of the transformer protection.
The fault current is high, and sometimes very high, but the changes in the phase
currents may be less than 10% of the rated current.
       Maintaining the quality of the power supply for sensitive industrial customers
as well as for general customers is a concern of transformer protection. The
transformer can withstand a very long duration of low magnitude through fault
current but even this may cause severe problems for motor driven industrial
processes, unless the fault is cleared in a short number of cycles with due care for
additional reactive power support.
        Another requirement is that transformer relay protection can be taken for
maintenance while the transformer is energized for critical installations. Because of
this it is required that the Main-2 protection schemes meet Main-1 requirements to
provide protection during maintenance. Normally this is done by grouping the
protections in two groups A and B that are not exactly duplicated but provide
redundant protection groups.

6.5   PROTECTION SCHEMES
This section covers the main types of transformer protection schemes. Each scheme
is reviewed to see its advantages and disadvantages as well as how they meet the
protective relaying requirements. These types are as follows:
•     Differential relay
•     Directional or Nondirectional phase over current relays
•     Ground fault protection (residual, neutral, restricted earth fault, or tank ground
      over current relays)
•     Directional or nondirectional earth fault relays
•     Mechanical type fault detectors (Buchholz, Oil level indicators, Pressure relief
      devices for transformer and Buchholz for OLTC) and overcurrent blocking
      relays
•     Over-excitation relays (Not necessary for transmission transformers or grid
      transformers)
•     Overload protections (Oil temperature winding temperature relays for
      transformer and for OLTC, over load relays)

                                 Chapter 6: Power Transformers                       67

•     Over-voltage relay for tertiary winding
      Some discussion on these relay elements is given below:

6.5.1 Transformer Differential Protection
Differential protection is the most commonly applied protection for transmission
transformers.
       There are two types of differential relays. Percentage biased differential relay
with harmonic restraint (2nd and 5th harmonic restraint) with a high set unit and high
impedance differential relay. For a multi-winding transformer only percentage biased
relay can be applied whereas for autotransformer both percentage biased and high
impedance relays can be used. The simplicity of comparing current into all terminals
of the transformer gives the differential relay very high reliability.
       In case of percentage biased differential relays current transformers or
auxiliary CT's in a delta connection have to be used at grounded transformer
windings to avoid false operation on external faults. The removed zero sequence
component, however, makes the transformer differential relay less sensitive.

      The differential relay protection does an excellent job of meeting a large
number of the protective relaying requirements, but must be combined with other
protective devices to provide full transformer protection.

6.5.2 Local Distance Relay Protection
Distance relays can be used as primary protection or as back-up protection for the
transformer. It consists of a multi-zone impedance relay on the HV side or on LV
side of the transformer looking into the transformer as shown in Fig 6.2.

                 HV                                               LV

                                 Zone-1 ~
         Zo~ Z<                  Zone-2
                Fig. 6.2 Distance relay protection

       The main advantages of the distance relay are, it provides back-up for remote
faults and protection for fault withstand. It also provides overlapping protection with
the bus protective zones by its reverse zone. This can be beneficial if the bus
protection is not duplicated and failure of bus protection to operate results in delayed
clearance of fault by over current relays on the other side of the transformer.

68                Manual on Reliable FauN C/eatanca and _-Up Protaction of
                            EHV and UHV Transmission Networl<s

      It has not been a practice to use this protection by utilities in India; however, it
can be considered on case-to-case basis. One of the main reasons for its usage can
be to provide substation back-up protection for bus faults.

      Coordination of Zone 2 / Zone3 timers with transmission line relays can be
problem and has to be taken care of. It must be noted that the distance relays
cannot provide sensitive ground fault protection.

6.5.3 Directional and Non-Directional Phase Over current Protection
The phase over current protection is a very inexpensive, simple and reliable scheme
for fault detection and is used for transformer protection applications. It can provide
limited overload protection but cannot provide instantaneous protection for all
internal faults. It can also provide back-up protection for bus bars.

      An additional high set unit is also usually provided. The instantaneous
elements help in providing high-speed clearance of heavy current faults that
threaten system stability.

       The relay suffers from having to be set very high for transformer inrush, for co-
ordination with down stream relays, and to allow transformer overloads. Therefore it
is ineffective for low magnitude internal transformer faults or phase to ground faults
on the low voltage side of the transformer.

      It does provide for transformer fault withstand protection and some limited
over load protection. It can provide back-up for failure of the switching device but
only with very long time delays. In some applications directional over current relays
are located on both the HV and LV sides of the transformer. Both relays are set to
see into the transformer. This allows better coordination with external over current
relays because of the need only to see part of the transformer windings.

       Numerical over current relays provide upgraded performance for transformer
back-up protection. The digital filters remove the DC component and harmonics from
the inrush current. Numerical back·up over current relays can therefore be set much
more sensitive than conventional types and are recommended to be used.

6.5.4 Ground Fault Protection
Various ground fault protections used are described below. Generally, these
protections are meant to provide the grounded winding with a low sensitivity ground
fault protection only. They do not provide other types of protection.

6.5.4.1 Zero Sequence Over Current Relays
Zero-sequence over current relays provide protection against internal phase-to-
ground faults. The neutral current or the residual current may energize the over

                              Chapter 6 : Pawsr Transfonnsrs                       69

current relay. The setting may be much lower than the rated phase current.
Harmonic restraint may be required to obtain sensitive settings. An additional high
set unit is also usually provided.

6.5.4.2 DIrectIonal or Non-DIrectIonal Earth Fault Relay
This type of protection is also specific to transformers with at least one directly
grounded or resistance grounded winding. The protection is specialized to protect
for winding faults to ground. The connections of the over current units can be only in
the neutral, or in the residual phase. These connections can be set much lower than
the phase over current because of the cancellation of the phase current.

      The sensitivity to the harmonic and inrush currents can be one of the main
problems with back-up ground over current relays. Settings must be able to allow
inrush, which usually means desensitizing the back-up relay. Static relays that do
not have filter for these harmonics usually can have problems. Numerical relay
offers the best characteristic since digital filters remove harmonics and DC offset
currents from the inrush and is, therefore, recommended.

6.5.4.3 Restricted Earth Fault Relays
      Zero- sequence differential relays (Restricted earth fault relay) provide best
protection against phase-to-ground faults in transformers connected to solidly
grounded systems or resistance grounded transformers. The residual current and
the neutral current energize the relay.

6.5.4.4 Zero Sequence Over Voltage Relays
Zero sequence over voltage relays provide protection against phase-to-ground faults
in transformers connected to non-effectively grounded systems or for delta
connected tertiary windings. The open delta voltage energizes the relay. A filter to
reject third harmonics may be necessary.

6.5.4.5 Tank Ground Fault Protection
This type of protection is specific to transformers with at least one grounded or
resistance grounded winding. The protection is specialized to protect for winding
faults to ground.

      The tank ground fault protection or tank leakage protection is a ground-
connected relay, which is connected in series with the main tank ground. The tank is
insulated from ground except for one path which has a current transformer around it
connected to the tank ground relay. The relay will see any current flowing from the
tank to the ground such as bushing failures, winding to tank failures, and core to
winding failures. Since minimum current flows through this path during normal
operation it can be set very sensitive. The problem with this protection is that it

70                Manual on Reliable FauN C/eatanca and _-Up Protaction of
                            EHV and UHV Transmission Networl<s

requires a single path to ground through at most 1 ohm resistance. This creates a
high voltage to remote earth from the transformer tank during ground faults, which
may cause safety problems. The path can easily be shorted out by inadvertent
control or metallic paths to the transformer case. Also care must be taken to prevent
maloperation from transformer tank capacitance currents.

      In general this protection is meant to provide a grounded winding with a low
sensitivity ground fault protection. It does not provide any other type of protection.

       It is not normal practice to use this protection by utilities in India but in some
cases, particularly where French practices are adopted, it has been used. According
to French practice normally any transformer winding fault other than inter turn fault
will invariably involve earth. And the probability of having phase-to-phase fault in 3
phase transformers is also quite remote. As such Tank Leakage protection relay
along with fire protection system (Drain and Stir Method) quite uniquely becomes the
main protection for the transformers.

6.5.6 Mechanical Type Fault Detectors (gas, oil, or fault pressure) and Over
      Current Blocking Relays
Transformer Buchholz protection, OLTC Buchholz Protection, Pressure Relief
devices, etc., fall in this class of protections. They are all designed to provide
protection for low magnitude turn-to-tum faults. These types of faults are not
covered by any of the other protection schemes. In addition to this specialized
protection they all provide some limited protection for insulation failure faults inside
the transformer tank. None of these protection schemes can detect faults outside the
transformer or inside the transformer bushings. All the schemes work on some type
of pressure differential or pressure rise of the oil or gas inside the transformer. The
pressure from the internal tank fault is used to identify the fault and provide fast
tripping before a major fault occurs.

       The gas accumulator relay (Buchholz Relay) also operates due to long-term
accumulation of gasses associated with overheating of various parts of the
transformer conductor and insulation systems. This will detect faults in their early
incipient stages and prevent significant damage.

      Some times security is a problem for these types of devices. The addition of
an over current blocking relay, which blocks or slows down the tripping of these
devices for high magnitude current flows for which the differential relay would
operate quickly, may be used to improve security of the devices. The problem is that
some internal faults may occur as a result of a through fault and the devices may
incorrectly block tripping. However if such maloperations are observed provision of
such blocking devices may be done on case-to-case basis.
      As stated before, generally these protections are mainly aimed at meeting
external safety requirements and for providing low magnitude turn-to-turn fault
protection.

                              Chapter 6 : Pawsr Transfonnsrs                       71

     For higher reliability, duplicating of the initiating contacts is sometimes done
and may be considered on a case-to-case basis.

      To avoid common failures and to allow optional gas collection from different
places in the tank, one of the utility provide in their system two Buchholz relays in
each tank, which are located in separate pipes from different areas of the tank to the
conservator. Further there are two PROs on each tank. This is because they feel
that these protection functions for sensitive internal fault detection cannot be
diversely covered and therefore need to be duplicated.

6.5.7 Over Excitation Protection
This is another type of specialized protective relaying application where only one
protective level is covered. No other relay provides adequate over-excitation
protection of the transformer core. Damage to the core laminations can occur if an
excitation larger than the VoltsiHertz rating of the transformer is reached. This type
of protection does not cover any requirements except this one.

       For grid transformers this protection may lead to cascade tripping due to the
fact that all the substation transformers subjected to over voltages coupled with drop
in frequency will be allowed to trip. An extract from CIGRE, SC-34 working group
report "Transformer overfluxing protection" from ELECTRA (N031), 1973 is
reproduced below:

        "Considering margins between rated and saturation flux densities previously
stated, it is concluded that, in general, no special over fluxing protection is
necessary for transformers connected to the system and this is confirmed by
literature and the replies from working groups enquiries"

        Presently it has been a practice to use over excitation relay for the grid
transformers. In view of the above reasoning this practice should be reviewed by the
utilities.

6.5.8 Overload Protection

6.5.8_1 011 Temperature Sensors

The top oil temperature sensors can detect overheating. The temperature limit
settings vary from utility to utility and also depend ullon manufacturer's
recommendations. Typical settings are 9SoC for alarm and 100°C for trip. Because
of the heating and cooling requirements of a transmission transformer some
specialized temperature protection is required to provide protection over the full
range of operating limits of the transformer. The transformer temperature depends
upon the ambient temperature, the cooling system condition, the excitation voltage
and the transformer load. To provide for temperature protection a sensor is usually
provided to indicate top oil temperature. The power transformers have a large

72                Manual on Reliable FauN C/eatanca and _-Up Protaction of
                            EHV and UHV Transmission Networl<s

thermal heat sink and can withstand overloads for certain limited time. Selective
protection, monitoring and load management are considered necessary. The tripping
of the transformer should be the last action.

6.5.8_2 WIndIng Temperature Sensors
Winding temperature sensors can detect overheating. The temperature limit settings
vary from utility to utility and also depend upon manufacturer's recommendations.
Typical settings are 100'e for alarm and 1Os'e for trip. To simulate the winding
temperature, a resistor sized to approximate the heating in the transformer winding
at full load is used. The resistor is fed by a current transformer from one of the
phase currents. To add oil temperature, the top oil is circulated in to a well within the
resistor. This combined heating of the resistor from transformer current and top oil,
is used to simulate the winding temperature.

      These two relays do not meet any of the other requirements but are again the
only relays which meet the over load temperature limit requirements.

     For higher reliability duplicating of the initiating contacts is sometimes done
and may be considered on a case-to-case basis.

6.5.8_3 Overload Relay
It is also a practice to use a simple over current relay with a time delay arranged to
give alarm to warn the operator of any overloading of the transformer. Use of
thermal relay to provide tripping is also practiced by some utilities.

6.6   TYPICAL MAIN-1 PROTECTION SCHEMES
Typical Main-1 schemes consist of
•     Differential protection for high magnitude intemal faults
•     Over current or impedance relays for through fault withstand protection
•     Over fluxing protection (Normally for Generator transformers only)
•     Buchholz gas-accumulator relay or sudden pressure relay for low current turn-
      to-turn faults
•     Top oil temperature sensor for over temperature protection
•     Winding temperature sensor for over temperature protection
•     Neutral or residual over current protection

                               Chapter 6 : Pawsr Transfonnsrs                        73

6.7   TYPICAL MAIN-2 AND BACK-UP PROTECTION SCHEMES
A true Main-2 protection scheme is usually not provided. The main reason is the low
probability of a relay failure during a protected event. Given the present record of
transformer protection this seems to be adequate to provide necessary reliability.
But as operating requirements change and single contingency limits are pressed the
level of Main-2 protection may need to be re-evaluated in future.
      Typical Main-2 schemes are made up of following:
•     Restricted earth fault protection
•     Directional over current and earth fault relays
•     Over fluxing protection (Normally for Generator transformers only)
The back-up schemes consist of following.
•     Non-directional or directional over current and earth fault relay
•     Distance relays
      In case of autotransformers, a 3-phase high impedance relay, which also acts
as restricted earth fault relay is used some times instead of a single element relay.
       The non-directional over current relays are used when they could be
coordinated with the over current protection on connecting lines. Coordination
requirements usually require the clearing times to be longer than the other types of
back-up protection. Directional over current relay improves the co-ordination by
being set to look through the transformer impedance. For this reason they are
normally used for all interconnecting transformers. When applied on both sides of
the transformer, the current levels where coordination with line relaying is required is
limited by the transformer impedance which greatly improves the tripping times for
higher current faults in the transformer. The directional ground over current relay can
be set much more sensitive and with very short time delays. For all interconnecting
transformers use of directional over current and ground over current relays with high
set units are recommended.
      There a number of general problems with back-up relay viz., the sensitivity to
the harmonic and inrush currents. Setting must be able to allow innush, which
usually means de-sensitizing the back-up relay. Numerical relays can filter
harmonics and DC offset currents from the inrush and therefore may be preferred.

6.8   RECOMMENDATIONS FOR MAIN and BACK-UP PROTECTIONS AND
      GROUPING OF THESE IN GROUP- A and GROUP-B
In the above paragraphs some important application aspects connected with the
transformer protection and some recommendations have been brought out and
these should be considered. Few of these are brought out below.
•     A true Main-2 protection scheme is usually not provided in case of
      transformers. But as operating requirements change and single contingency

74               Manual on Reliable FauN C/eatanca and _-Up Protaction of
                           EHV and UHV Transmission Networl<s

      limits are pressed the level of Main-2 protection may need to be re-evaluated
      in future.
•     Numerical relays offer the best characteristic since digital filters remove
      harmonics and DC offset currents from the inrush. Numerical back-up over
      current relays can therefore be set much more sensitive than conventional
      types and are recommended to be used.
•     Harmonic restraint may be required to obtain sensitive settings in case of zero
      sequence over current relays ..
•     Some times security is a problem In case of Buchholz relays. The addition of
      an over current blocking relay, which blocks or slows down the tripping, may
      be used to improve security of the devices.
•     In case of mechanical type of fault detectors like Buchholz and PRDs, for
      higher reliability, duplicating of the initiating contacts may be considered on a
      case-to-case basis.
•     For grid transformers, application of over excitation protection not considered
      necessary and present practice of providing it should be reviewed.
•     The power transformers have a large thermal heat sink and can withstand
      overloads for certain limited time. Selective protection and monitoring and load
      management is necessary. The tripping of the transformer should be the last
      action

      Fast clearance of faults in the transformer is important for stability of the
system and therefore adequate protections should be provided. Requirement of
through fault withstand is also important and should be considered.

       As per the current practice, it is common to group various main 1, main 2 and
back-up transformer protections at 765 kV, 400kV and 220 kV in two groups of
protections (Group A and Group B) connected to separate DC sources and separate
master trip relays. This should cover, to some degree, the need for maintenance of
protective equipment with the transformer energized. No change is proposed in this
practice. Reference may be made to CBIP Manual No 274 "Protection of
Generators, Transformers and 220 kV and 400 kV Networks". Which gives details of
current practices being followed. Where Fire protection is provided the contacts
should be wired to trip both Group-A and Group-B trip relays.

      For 132 kV level transformer where two separate DC sources are not
provided, it is recommended that the protections be grouped in two groups
connected to separately fused DC sources. One gets to use two trip relays in this
case, which is advantageous.

## Chapter 7: Shunt Reactors

SHUNT REACTORS
Shunt reactors are used to compensate for capacitive shunt reactance of
transmission lines and cables. They absorb reactive power especially during over
voltage conditions and thus help maintaining system voltage within limits. There are
two main types of shunt reactors, dry air-core type and oil-filled air-core and gapped-
core types.

       The oil-immersed shunt reactors are generally V-connected with a solidly
grounded or impedance-grounded neutral and connected without any controlling
circuit breaker directly to either ends of the EHV lines.

       The dry type reactors or oil-filled reactors of 11 kV or 33 kV ratings are
normally ungrounded star, connected through controlling circuit breakers of suitable
TRV ratings to the tertiary of Inter-connecting transformer (ICT) of 400 kV I 220 kV
ratio purely for reactive power consumption to control the voltage profile during light
load conditions. However the practice in India has been so far to use only oil
immersed reactors connected to the tertiary terminals because of non availability of
proven design of air-core reactors of higher ratings at medium voltages indigenously
even for such applications.

      The reactor bank protection considerations are a subset of the transformer
protection and many similarities exist.

7.1   REACTOR CONSTRUCTION
Dry-type shunt reactors of 11 kV and 33 kV ratings are considered very effective and
widely used in Static Var Systems or Compensators and also for absorbing reactive
power during light load conditions that cause higher voltage levels. The primary
advantages of dry-type air-core reactor, compared to oil-immersed types, are lower
initial and operating costs, lower weight, lower losses, and the absence of insulating
oil and its maintenance. The main disadvantages of dry-type reactors are limitations
on voltage and kVA rating and the high-intensity magnetic field. There is no
magnetizing inrush current when the reactor is energized.

       Oil-immersed shunt reactors are either coreless type (air core design) with
linear characteristics at least up to 1.5 pu or gapped iron-core type with linearity
restricted to 1.2 - 1.3 pu. Both designs are characterized by low frequency long time
constant current when de-energized, which is determined by the parallel
combination of the reactor's inductance and the line capacitance. The gapped iron-
core design has a more severe energizing inrush than the air core or core-less type.
Both designs are constructed to provide linearity of inductance and to reduce

76                Manual on RsliabIB Faun C/sarancs and Back-Up Protection of
                             EHVand UHV Transmission Networlrs

residual or remnant flux when compared to a transformer or reactor without gapped
core. Both design are constructed for either self-cooling or forced cooling. Normally
most of the reactors used in India are natural cooling type. It may be mentioned that
in air core design there is no iron core in the main circuit flux path but liberally
designed strong tank shields of either CRGO or sometimes copper are usually
provided. For control of switching surge over voltages, gapped core reactors with
knee-point voltage of 1.2 or 1.3 provide better results. While shunt reactors of
coreless type with linearity 1.5 pu are used for reactive power absorption.

      The shunt reactor construction has been quite complicated in view of control
of core or tank vibrations within stringent limits and the duties to be performed to
withstand the severe over voltages during switching-on or load rejections. There has
been good statistics of failures of shunt reactors attributable to either construction
complications or system operational severity

7.2   SHUNT REACTOR FAILURE MODES AND RATES
Before discussing the reactor failure rates it is important to understand the modes of
reactor failure. The oil-immersed reactor faults can be broken into four categories:
•     High current phase-to-phase and phase-to-ground faults.
•     Turn-to-turn faults within the reactor winding.
•     Miscellaneous failures such as loss of cooling or low oil
•     Failure due to increased core and tank vibrations beyond the permissible
      limits

       Because of the proximity of the winding with the core and tank, winding-to-
ground failures can occur. The magnitude of this fault decreases as the location of
fault moves closer to the neutral side of the reactor.

      Turn-to-turn faults cause only small change in phase currents. The current in
the short-circuited fault path would be quite high but will obviously not show as
increase in the line current. This increases rapidly the operating oil and winding
temperature, increases the internal pressure, and causes accumulation of gas. If
these are not quickly detected they will evolve into a major fault.

     The failure rates of oil-immersed reactors are quite high ranging from 3% to
5% per year.

7.3   TYPICAL SHUNT REACTOR ARRANGEMENTS
There are two main arrangements for shunt reactor connection. The first is 11 kv or
33 kV tertiary connected shunt reactors and the second is directly connected shunt
reactor, connected to EHV system either through a controlling circuit breaker, called

                                Chapt.r 7 : Shunt Reactors                          77

switched type and the other directly connected to the line through an isolator called
unswitched reactors.

     The tertiary supplied reactor bank is provided with a circuit breaker of suitable
TRV ratings on tertiary side.

      The second method of connecting shunt reactor is to connect it to one or both
ends of a long transmission line or cable. These reactors are usually V-connected
with either a solidly grounded neutral or grounded through a reactor of suitable
impedance value. The neutral reactor connected between the star point of EHV
shunt reactor and the ground limits the secondary arc current to a low value of
around 10 amperes typically for 400 kV system to ensure complete de-ionization of
arc path when EHV system develops a single line to ground fault. Arc extinction
during line single-phase autoreclose dead time is assisted by this neutral reactor.

    In the event of a fault in the unswitched shunt reactor itself, transfer trip
command will be required to trip the remote end breaker.

7.4   SHUNT REACTOR PROTECTION REQUIREMENTS
Protection requirements for shunt reactors fall into five areas: high magnitude
phase-to-phase faults, low magnitude phase to ground faults, tum-to-turn faults, and
other miscellaneous failures.

       High magnitude phase faults in shunt reactors are required to be
cleared based on the same criteria used for the primary equipment supplying the
reactor. For the tertiary supplied reactor the fault withstand of the transformer must
be considered the limit for the clearance time. The tertiary winding is quite sensitive
to phase-to-phase or three phase faults. As such efforts should be made to ensure
that tertiary does not suffer such faults. It is important to note that all the faults
extemal to tertiary must be contained as always to a single phase to ground fault.
For the direct connected oil-immersed reactors, that are unswitched EHV reactors,
the critical clearance time shall of the same order of magnitude as applicable to EHV
Lines.

      The single phase to ground fault in the system external to tertiary tenninals
shall normally be of very low fault current amplitude. Such faults must, however, be
detected and isolated to ensure that this does not lead to phase-to-phase or three
phase faults. The detection of turn-to-turn fault in the shunt reactor is rather tricky
and cannot be detected by conventional differential protection. The gas pressure
increase or rate of gas generation or the fall in reactor impedance gives a better
indication and criteria for such protection.

78                Manual on RsliabIB Faun C/sarancs and Back-Up Protection of
                             EHVand UHV Transmission Networlrs

      Miscellaneous failures such as low oil level, high winding temperature or oil
temperature are usually set to alarm at a set level and to trip once the oil level or the
reactor temperature reaches the next level of setting.

     The reactors, whether unswitched type provided on lines or switched type on
bus bars or on tertiary of the transformers, playa very important role to control the
overvoltages on switching or on load rejection or for enabling black-start of the
network or for controlling the voltage profile of both the up-stream or down-stream
system.

      The reactors therefore playa very active role to ensure satisfactory operation
of the power system. Based on the types of failures described above and the basic
design of the shunt reactors to satisfy the requirements of power system, the
protective relaying schemes for the shunt reactors should meet the following key
requirements.
•     Maintain transient fault and voltage stability of the power system
•     Prevent unnecessary false tripping of the transmission reactor during critical
      load periods
•     Maintain required quality of supply
•     Provide for maintenance of protective equipment with primary equipment
      energized by providing two groups of protections

       Shunt reactors have to remain in service with active protection remaining
vigilant and fully operational. The direct tripping command to trip the remote breaker
has to be through coded and secure signal via information link. The power system
cannot tolerate false trip command creating outage of the line.

      For smooth control of voltage profile during peak and off peak hours frequent
switching of shunt reactors provided on the bus bars or on transformer tertiary will
be required and the system should not fail on account of such frequent operation of
shunt reactors. The tough duty of circuit breakers for control of switched shunt
reactors with good margin in TRV requirements and switching cycle should be
recognized.

     The provision of Main 1 and Main 2 Protection system for the Shunt Reactors
must meet the same criteria as provided for the line and transformers.

     The protection system must satisfy the following types of faults specific to the
Shunt Reactors:
•     Protect for internal phase to ground or phase to phase faults
•     Protect for external tank faults to ground or phase to phase faults

                                 Chapt.r 7 : Shunt Reactors                           79

•     Protect for internal partial winding or turn-to-turn faults.
•     Limit top oil temperature to maximum temperature limit
•     Vibration monitoring of core and tank wall
•     Prevent rupture of reactor tank during internal fault
•     Provide for failure of an interrupting device
•     Provide for over-excitation of reactor core

      The switching device TRV should match with specific requirement of reactor
current switching. The knee-point voltage of shunt reactor and linearity selected
should match with the requirement of the system where the reactor is located for
adequate protection against over voltage and consequent overloads.

7.5   PROTECTION SCHEMES
This section covers the main types of reactor protection schemes. Each scheme is
reviewed to see its advantages and disadvantages.

      The protection schemes generally are as follows:
•     Differential relay for phase to phase and phase to ground faults
•     Impedance relay for tum to turn faults and back-up protection or phase and
      ground over current relay
•     Ground fault protection by Restricted earth fault, or Neutral displacement relay
•     Mechanical type fault detectors (Buchholz, Oil level indicators, Pressure relief
      devices)
•     Oil temperature and winding temperature relays
•     Peak-to-peak amplitude of vibration and tank monitoring

      Some discussion on these relay elements is given below:

7.5.1 Reactor Differential Protection
Differential protection is the most commonly applied protection for Shunt reactors.
Generally, the differential relays provide quick clearance of phase-to-phase and
ground faults.

7.5.2 Impedance Relay
Impedance relays are used as primary protection or as back-up protection for the
reactor. It is also used for detecting turn-to-tum faults within the reactor. Such relays

80                Manual on RsliabIB Faun C/sarancs and Back-Up Protection of
                             EHVand UHV Transmission Networlrs

also monitor the faults inside the reactor at some good percentage of winding faults.
Turn-to-turn faults inside reactor winding may not change the through current of the
reactor but the impedance values change drastically up to at least 50 % of
impedance of the reactor. It consists of a single or preferably a two-zone impedance
relay on the high side of the reactor looking into the reactor.

       The impedance relay has some benefits of providing high speed tripping in the
Zone-1 protection and slower speed tripping in Zone-2. It must not be set to operate
for inrush characteristics during reactor energization or de-energization. The setting
of the relay has to be coordinated while taking into account the energizing and d-
energizing transients.

7.5.3 Phase Over Current Protection
The phase over current protection is a very inexpensive, simple, and reliable
scheme for fault detection and is used for some reactor protection applications as a
back-up protection. The setting must be high enough to prevent inrush currents from
causing unwanted operation. When used it should have both instantaneous and time
delayed elements. The instantaneous elements help in providing high speed
clearance of heavy current faults which threaten system stability.

7.5.4 Ground Fault Protection
The ground fault protection within the shunt reactor is best provided by simple
conventional Restricted Earth Fault (REF) relay selected and set on the same
philosophy as for transformer REF. For tertiary connected reactors neutral over
voltage relays are used. Some times a ground over current relay is used as a back-
up protection when phase overcurrent protection is provided.

7.5.4_1 Restricted Earth Fault Relay
Zero-sequence differential relays (Restricted earth fault relay) provide protection
against phase-to-ground faults in shunt reactors supplied from solidly grounded
systems. Generally, this protection is also provided for EHV shunt reactor with
Neutral Grounding reactor connected between star point of shunt reactor and
ground.

7.5.4_2 Zero Sequence Over Voltage Relay
Zero-sequence over voltage relays provide protection against phase-to-ground faults
on reactors supplied from non-effectively grounded systems. The open delta voltage
energizes the relay. A filter to reject third harmonics may be necessary. The contact
is connected to give alarm only.

                               Chapt.r 7 : Shunt Reactors                          81

7.5.4.3 Ground Overcurrent Relay
The ground over current protection is a very inexpensive, simple, and reliable
scheme for fault detection and is used for some reactor protection applications as a
back-up protection for phase-to-ground faults. This is used in conjunction with phase
over current relay. When used it should have both instantaneous and time delayed
elements.

       The sensitivity to the harmonic and inrush currents is one of the main
problems with back-up ground over current relays. Settings must be able to allow
inrush, which usually means desensitizing the back·up relay. Numerical relay offer
the best characteristic in this area since the digital filters remove harmonics and DC
offset currents from the inrush and are, therefore, recommended.

7.5.5 Mechanical Type Fault Detectors (Buchholz, Oil Level Indicators,
      Pressure Relief Devices)
These relays to be provided on shunt reactors of medium to high capacity are quite
similar to those provided on power transformers.

      For higher reliability duplicating of the initiating contacts is sometimes done
and may be considered on case-to-case basis depending upon the location and size
of shunt reactors and voltage class.

      To avoid common failures and to allow optional gas collection from different
places in the tank, one of the utility provide in their system, two Buchholz relays in
each tank, which are located in separate pipes from different areas of the tank to the
conservator. Further there are two PRDs on each tank. This is because they feel
that these protection functions for sensitive internal fault detection cannot be
diversely covered and therefore need to be duplicated.

7.5.6 Over Excitation Relay
The over voltage relays provided on the line or on transformers take good care of
shunt reactor over-excitaiton. It should however be noted that shunt reactors are
most required during over voltages as they control and limit the over voltages even
control the runaway voltage levels by providing more short time reactive power to
system when subjected to over voltages. Any tripping of the reactor under
overvoltage condition would only worsen the situation.

7.5.7 Top 011 and Winding Over Temperature Protection
The protections provided on shunt reactors are exactly similar to that provide on
power transformers and criteria for selection and setting should therefore be the
same

82                Manual on RsliabIB Faun C/sarancs and Back-Up Protection of
                             EHVand UHV Transmission Networlrs

      For higher reliability duplicating of the initiating contacts is sometimes done
and may be considered on case-to-case basis depending upon then location and
size of shunt reactors and voltage class.

7.6   TYPICAL MAIN-1 PROTECTION SCHEMES
Protection schemes for the reactor bank must provide for full protection during fault
conditions. In addition, back-up protection should be provided when the potential for
a failure to trip exists.
      Typical Main-l schemes consist of:
•     Differential protection for high magnitude intemal faults
•     Over current or impedance relay for through fault withstand protection
•     Buchholz gas-accumulator relay or sudden pressure relay for low current turn-
      to-turn faults
•     Top oil or winding over temperature protection for temperature protection
•     Neutral over current protection or Neutral over voltage relay as ground fault
      protection.

7.7   MAIN-2 AND BACK-UP PROTECTION SCHEMES
A true Main-2 protection scheme is usually not provided. The main reason is the low
probability of a relay failure during a protected event. Given the present record of
reactor protection this seems to be adequate to provide necessary reliability. But as
operating requirements change and single contingency limits are pressed the level
of Main-2 protection may need to be re-evaluated in future.

      For the direct connected oil-immersed reactors typical Main-2 protection
consists of:
•     Restricted earth-fault protection, high impedance type, covering the neutral
      reactor as well as the main reactor.
•     Sudden pressure or gas accumulator relay for limited turn-to-tum faults.
•     The back-up protection is provided with Impedance relay set with a time delay
      between 0.7 to 1.0 second and an impedance setting of 60% of the reactor
      impedance.
Or
•     Instantaneous and time delayed over current for phase and ground

                               Chapt.r 7 : Shunt Reactors                           83

      The neutral reactor is not stressed under nonnal conditions and is normally
protected only by Buchholz relay in the Main-1 protection scheme, and oil
temperature in the Main-2 scheme.

7.8   RECOMMENDATIONS FOR MAIN AND BACK-UP PROTECTIONS AND
      GROUPING OF THESE IN GROUP- A AND GROUP-B
In the above paragraphs some important application aspects connected with the
reactor protection and some recommendations have been brought out, and these
should be considered. A few of these are, brought out below:
•     A true Main-2 protection scheme is usually not provided in case of reactors.
      But as operating requirements change and single contingency limits are
      pressed the level of Main-2 protection may need to be re-evaluated in future.
•     In place of impedance relay a phase and ground over current protection can
      also be used as back-up protection.
•     Numerical relays offer the best characteristic since digital filters remove
      harmonics and DC offset currents from the inrush. Numerical back-up phase
      over current and ground over current relays can therefore be set much more
      sensitive than conventional types and are recommended to be used.
•     The over voltage relays provided on the line take good care of shunt reactor
      overexcitaiton. Therefore separate over excitation protection is generally not
      considered necessary.
•     In case of mechanical type of fault detectors like Buchholz and PROs, for
      higher reliability, duplicating of the initiating contacts may be considered on a
      case-to-case basis

      Fast clearance of faults in the reactor is important for stability of the system
and limiting equipment damage. Therefore adequate protections should be provided.

      The reactors are normally used in 400 kV and 765 kV networks. As per the
current practice it is common to group various Main-1, Main-2 and back-up reactor
protections in two groups of protections (Group A and Group B) connected to
separate DC sources. No change is suggested in this practice. This should cover to
some degree the need for maintenance of protective equipment with the reactor
energized. Reference may be made to CBIP Manual No 274 "Protection of
Generators, Transfonners and 220 kV and 400 kV Networks·, which gives details of
current practices being followed.

## Chapter 8: Busbars

BUSBARS
       Bus bars are the node points of a power system at which large amounts of
electrical energy are concentrated. Some bus bars have often been left without
dedicated local protection, since the occurrence of faults in the bus-zone is
commonly considered as being of low probability, and the fear of unwanted
operation has outweighed its advantages. The unplanned or nonselective outage of
the bus bar can lead to the loss of power supply to a widespread area. The effect of
a fault within a bus-zone can however be potentially far more damaging than faults
on other items of primary plant. The failure to clear a bus fault can lead to
considerable equipment damage and system instability.

      In the case where no local bus bar protection is employed, bus-zone faults
would be cleared by the back-up or system protection. In some cases this may
indeed suffice, e.g., at lower voltage levels, but for higher transmission voltages
where security of supply is of paramount importance and fault current levels are
high, the non-discriminative fault clearance and relatively slow clearance times
would be unacceptable.

      Where local bus bar protection is employed, the zone of protection will include
switching devices (bus selector, bus section disconnectors, circuit breakers,
grounding switches), parts of the CT on the bus side of the core used for bus bar
protection, other connecting parts of the bus, in addition to the bus bars themselves.

        Bus bar protection is expected to detect and clear all shunt faults i.e., phase to
ground and phase-to-phase faults within the assigned bus bar zone bounded by the
respective locations of the current transformers. Faults can be caused by the failure
of an item of primary system plant or human error, e.g., a forgotten grounding clamp
following maintenance work. Flashover due to external causes, e.g., dropping of
wires by birds, electrocution of birds and monkeys are also major causes for bus
faults.

      The protection is not normally required to clear open phase faults, i.e., an
unbalance in the phase impedances usually caused by the interruption of one or two
phases. Detection and clearance of such series faults are to be done by protections
provided for other power system objects.

       Although a number of methods of bus bar protection are available, all are unit
protection schemes. Back-up protection is provided either by duplicating the local
scheme, thereby preserving fast fault clearance, or by reverse zone of line distance
protection, or by time delayed distance relays in the remote stations, or by
directional back-up over current relays.

86                 Manual on Rs/iable Faun CIBar.mce and Back-Up Protsction of
                              EHVand UHV Transmission Networks

B_1     TYPICAL BUSBAR ARRANGEMENTS
Substations are either air-insulated (AIS) or metal-clad. Metal-clad switchgear is
nowadays mainly gas-insulated (GIS) using SF., as the insulating medium. There
are various types of substation construction. This depends partly on the bus bar
arrangement as well as other specific considerations such as the available space.
The bus bars in air-insulated substations are either made from ACSR conductors or
for higher current levels from tubing made of aluminium but rarely copper. SF. gas-
insulated switchgear may house all three phases together in a three-phase
enclosure, or for voltage levels above, typically 132 kV, separately in single-phase
enclosures. In the latter case the faults in the bus-zone can only be ground faults.

      Many different bus bar arrangements have evolved over the years, but the
most common bus bar arrangements are as follows:
•     Single bus - single breaker (also with bus-section circuit breakers)
•     Double bus - single breaker
•     Double bus - double breaker
•     Main and transfer bus (one or several main buses)
•     Double bus - one and a half breaker
•     Ring bus bar I four-breaker mesh

B.1.1 Location of Current Transformers

The location of a current transformer in relation to its circuit breakers in a station
partly determines the limits of protected zone and all the breakers falling within this
zone must be tripped in the event of a fault.
       Usually the CT is located after the circuit breaker in order to cover faults in the
breaker and the bay equipment by the bus bar protection. In this case (Fig. 8.1, a),
faults between the CT and the circuit breaker will be detected by the bus bar
protection. After tripping of the circuit breakers associated with the measurement
zone, the fault will continue to be fed from the remote end of the feeder. Further
tripping is required in order to clear the fault. Usually this is through circuit breaker
failure protection relay (LBB) initiating remote trip, or in its absence by back-up
protection. In the case of a line feeder, for example, a transfer trip command is sent
to the remote station to open the circuit breaker at that end of the line and to block
autoreclosure.
       If the circuit breaker is situated on the feeder side of current transformers
(Figure 8.1, b), faults between the breaker and CT will be outside the measurement
zone of the bus bar protection. Such a fault must therefore be cleared by the
protection system of that feeder and appropriate arrangements to trip the other
circuit breakers connected to the bus bar usually by a circuit breaker-failure
protection relay or a relay of similar design.

                                      Chapter 8 : Busbars                             87

                              (a)                           (b)

                 Fig. 1 Location of current transformer in feeder

      In double bus-bars scheme with bus coupler, the CTs are located on both
sides of bus section breaker, which facilitates overlapping of the two zones of
protection and avoid blind zone. However it is also common to provide CT on only
one side of the circuit breaker to reduce costs. In this case the fault between the CT
and the circuit breaker will have to be cleared by breaker fail relay or logic similar to
it.

8.2   FAILURE STATISTICS
The probability of bus bar faults is generally low. Detailed failure rate statistics for
faults on bus bar are usually not kept by the utilities. The worldwide survey shows
that dependability figures vary from 92 to 99.8% and security figures from 84 to
91.8%. The failure rates range from 0.5 to 2 faults per 100 bays per year.

8.3   BUSBAR PROTECTION REQUIREMENTS
A bus bar protection must be capable of clearing all phase to ground faults, and also
phase-to-phase faults where they can occur. Due to the fact that the short-circuit
levels of bus bar are often very high, bus bar fault clearance times are required to be
as short as possible. In many cases the required fault clearance times are always
kept at the minimum, rather determined by the fault withstand capability and by
considering the stability requirements.

       In SFs gas insulated switchgear; there is the possibility that an uncleared
arcing fault could cause a rupture (burn-through) of the enclosure wall. This happens
once the arc becomes stationary. The total 'burn-through time' is influenced by a
number of factors, e.g., how long the arc was mobile before becoming stationary,
fault current, gas pressure, and thermal diffusivity of the wall material.

      The protection must remain stable during through-faults (outside the bus-

88                 Manual on Rs/iable Faun CIBar.mce and Back-Up Protsction of
                              EHVand UHV Transmission Networks

zone) especially in the case of CT saturation and switching operations. Due to the
high ratio of through-faults to bus faults, bus bar protection is called upon to stabilize
many more times than it has to operate.

       Bus bars are divided into zones, the boundaries of which are defined by the
disconnectors or circuit breakers and their associated current transformers. Each
zone therefore requires an independent zone of protection so that fault clearance is
selective, that is, only those circuit breakers defining the boundary of the protected
zone are tripped. With the exception of simple bus bar configuration (single bus bar
and breaker and a half), these boundaries are not fixed and rather depend on the
position of the bus selection isolators. For this reason, the bus bar protection must
possess an accurate replica of the station's primary bus configuration.

       Information regarding the position of bus selection isolators is taken from their
auxiliary contacts and used in a logic, which ensures that the correct currents are
combined for each zone of measurement and the correct breakers are tripped in
case of a fault in that zone.

       To avoid malfunctioning of the scheme during on-load circuit switching from
one bus to another, the isolator auxiliary contacts should 'make before' and 'break
afte~ the main contacts during the isolator making and breaking operation
respectively. The position of the isolator making must be stored in case auxiliary
contact voltage supply fails. Such arrangements require very sturdy and reliable
isolator contacts. Now with numerical relays replica of such auxiliary contacts can be
provided in the scheme more accurately and reliably.

8.4   PROTECTION SCHEMES
Local main bus bar protection is employed in the high voltage substations. Where
clearance time and selectivity requirements are not critical, specially at lower voltage
level such as 132 kV, bus bars can be protected by distance relays in the remote
stations, or by reverse looking zone of local distance protections. Such protection
scheme has longer time of operation, of the order of 300 to 500 milliseconds

      For bus bars of strategic importance at 220, 400 kV and 765 kV levels, a
dedicated bus bar protection is provided. These bus bar protection schemes can
generally be categorized as high-impedance (in older verSion), low-impedance and
moderate-impedance (effectively a combination of plain circulating current and
biased differential scheme) and now numerical bus bar protection schemes.

8.4.1 High Impedance Circulating Current Protection
High impedance bus bar protection is widely used due to its simplicity and inherent
through-fault stability during CT saturation. In the case of CT saturation caused by
high through-fault current, the CT secondary impedance is reduced to the resistance
of its secondary winding. The measuring circuit comprises a high impedance-

                                   Chapter 8 : Busbars                                89

stabilizing resistor connected across the circulating current arrangement of all the
CT's in parallel. The value of the stabilizing resistor is chosen such that the voltage
drop across the relay circuit is insufficient to operate the relay for faults outside the
protection zone.

      If CT secondary switching is applied, a check zone measurement connected
to separate CT cores is usually added. The check zone measurement is an overall
measurement taken over the whole substation and is, by definition, independent of
the isolator's positions and auxiliary contacts. A trip command is only given when
both discriminating and check systems operate. Sometimes the relay setting is
increased to value higher than the heaviest loaded feeder current and check zone is
dispensed with. It should be noted that this would raise the minimum operating
current.

       An advantage of this scheme over low and moderate impedance scheme is
that the primary operating current can be set much below the circuit load resulting in
a high sensitivity.

        Disadvantages of this scheme are that the relay setting must take the CT
secondary winding and wiring resistances into account, which must be kept low, and
the CT knee point voltage must be known and is generally required to be high. All
CT's should have the same ratio (no turn correction) and should be of the same type
and performance (lOW stray impedance and of class PS or TPS). Furthermore, the
stability of the protection is dependent on the fault level.

     For the above reasons high-impedance bus bar protection is not
recommended when CT ratios are different and for complex bus bar arrangements.

8.4.2 Moderate Impedance Protection
Many of the limitations of high impedance protection can be overcome using
moderate impedance protection (or stabilized high-impedance scheme), which is a
combination of the normal high-impedance and stabilized differential schemes.
Although heavy through fault currents may produce a differential current that
exceeds the differential pick-up setting, the stabilizing current prevents tripping. The
requirements made on the primary CT's are subsequently less stringent than for a
simple high-impedance scheme.

8.4.3 Low Impedance Protection
Low impedance protection is the general name given to those schemes that do not
employ a stabilizing resistor, rather utilize current directly from the CT's. A number of
different measurement principles are employed in low impedance schemes.

90                 Manual on Rs/iable Faun CIBar.mce and Back-Up Protsction of
                              EHVand UHV Transmission Networks

8_4_3_1 Current Differential Protection
This type of protection is also known as current comparison with current restraint,
biased or percentage differential relaying. The operating current is the phasor sum
of all feeder currents and the restraint current is the arithmetic sum. A trip command
is given when the operating current is greater than its pick-up level (calculated from
the minimum bus bar short-circuit current) and the stabilizing factor, the ratio of
operating current to restraint current, exceeds its selling (typically 0.7 to 0.9).

      In the case where CT ratios differ, the currents have to be balanced by using
interposing CT's. In newer numerical protection equipment this is accomplished
internally.

      Whereas for high impedance protection the scheme is inherently stable during
CT saturation, in this scheme special measures must be taken to ensure the
protection remains stable during CT saturation.

       As with high impedance protection a check feature independent of the isolator
position can be used, or the protection can be complemented by a phase
comparison measurement.

8.4.3_2 Phase Comparison Protection
The measuring principle for phase comparison protection is based on the
assumption that the feeder currents are phase coincident during a bus bar fault. The
duration of phase coincidence of all feeder currents is checked for positive and
negative half-cycles. In addition the non-coincidence is used as a blocking signal.
The differential current can also be included in the phase comparison, thereby
further improving stability. The pick-up level is set above the load current.

8.4.4 Gas Density Detectors in GIS Switchgear
Gas density detectors are normally used to activate alarm under low gas density
conditions. These are used for protection purpose by providing several levels of
detecting SF. gas denSity. Stage 1 gives alarm when SF. pressure comes below a
certain value. When gas density falls further (Stage 2), it may not be possible to
extinguish an arc in the SF. gas in the event of a fault. Therefore in such case a trip
command is sent to that circuit breaker. In stage 3 where the SF6 gas density is so
low that it is unsafe even to trip the circuit breaker, a trip signal is sent to the
adjacent breakers and to the remote station (inter trip).

8.4.5 Supervision and Alarm Functions
The correct operation of bus bar protection employed in complex bus bar
arrangements relies on the protection having a faithful reproduction of the station
configuration. If this is not the case, false tripping or unselective tripping can occur.

                                  Chapter 8 : Busbars                               91

For this reason, the position of the bus selectors is ideally given by the combination
of two auxiliary contacts, one reporting 'isolator open', the other 'isolator closed'.
The voltage from these two contacts is supervised by an auxiliary relay and a timer
combination to ensure that an alarm is raised if, for example, the isolator does not
reach its end position or a wire from the auxiliary contacts becomes detached. In the
case of such an alarm, no further switching should take place, since this could under
some circumstances lead to false tripping. This alarm is often used to block the
protection.

      Protection schemes using differential current as the operating quantity also
use it to supervise the current transformer secondary circuits. The corresponding
alarm can also be used to block the protection.

       In high impedance schemes, a low set voltage relay with time delay,
connected across the main relay is used to detect a CT open circuit. It is made to
short the secondary bus wires, with a time delay to prevent malfunction of the total
scheme during through faults. The defective zone relay alone cannot cause tripping
due to the presence of check zone relay, the contact of which is wired in series with
the main zone relay. The time delay set on this low set relay ensures that it does not
give unwanted alarm in the event of an internal fault.

8.5   BACK-UP PROTECTION
It is possible to provide back-up protection of bus bars by duplicating the dedicated
protection or by using elements of line protections like reverse zone of local distance
protections or Zone 2 of remote end protections.

8.5.1 Duplication of Local Bus bar Protection
For substations of high strategic importance or where the bus arrangements are
complex, the complete bus bar protection can be fully duplicated. This is the
preferred approach at bulk transmission voltage levels.

      In cases where the bum-through time of SF6 switchgear is considered to be
shorter than the tripping time from remote back·up protection, then also the local bus
bar protection must be duplicated.

       Duplicated protections invariably employ separate DC circuits and CT cores.
They send trip impulses to separate trip coils and use separate isolator position
auxiliary contacts. Cross tripping of both trip coils is also done.

8.5.2 System Protection
Where clearance time and selectivity requirements are not critical, bus bars can be
protected by overreaching (Zone-2) element of distance relays in the remote
stations. Tripping is therefore at the remote stations, thereby disconnecting more

92                Manual on Reliable Faun CIBar.mce and Back-Up Protsction of
                             EHVand UHV Transmission Networks

transmission lines and loads than is actually necessary, and tripping times are
typically from 300 to 600 ms.

       For the majority of substations, especially those at lower transmission voltage
levels, back-up protection is provided by the system protection, i.e., remote-end
distance relay overreaching elements (second zone). A reverse looking element of
the local distance relay may be arranged to provide substation local back-up
protection.

       Where the main bus bar protection is provided by the second zone elements
of distance relays (i.e., when no bus bar protection is provided), back-up protection
can be considered as being provided by the 3'" zone elements of distance relays in
the more remote stations.

8.6   RECOMMENDATIONS FOR PROVISION OF BUS BAR PROTECTION
If left uncleared, the effect of a fault in a bus-zone can be potentially far more
damaging than faults on other items of primary plant. The unplanned or unselective
outage of the bus bar can lead to the loss of power supply to a widespread area.
The failure to clear a bus fault can lead to considerable equipment damage and
system instability. Therefore bus bar protection has an important role to play.

      In the above paragraphs some important application aspects connected with
bus bar protection and some recommendations have been brought out, and these
should be considered. A few of these are brought out below.

•     A dedicated bus bar protection shall be provided where security of supply is of
      paramount importance, fault current levels are high, and the non-
      discriminative fault clearance and relatively slow clearance times are
      unacceptable.
•     Bus bar protections being of unit type, back-up protection is provided either by
      duplicating the bus bar protection, or by reverse zone of line distance
      protection, or by time delayed distance relays in the remote stations, or by
      directional back-up over current relays.
•     Where the main bus bar protection is provided by the second zone elements
      of distance relays (i.e., when no bus bar protection is .rrovided), back-up
      protection can be considered as being provided by the 3 zone elements of
      distance relays in the more remote stations.
•     For substations of high strategic importance or where the bus arrangements
      are complex, the complete bus bar protection should be fully duplicated.
•     In cases where the burn-through time of SF. switchgear is considered to be
      shorter than the tripping time from remote back-up protection, then also the
      bus bar protection must be duplicated.

                                  Chapter 8 : Busbars                               93

•     High-impedance bus bar protection is not recommended when CT ratios are
      different and for complex bus bar arrangements.

      As per the current practice bus bar protection is provided for all substations at
765 kV, 400 kV, 220 kV and for generating station switchyards. No change is
proposed in this practice. Reference may be made to CBIP Manual No 274
·Protection of Generators, Transformers and 220kV and 400kV Networks' which
gives details of current practices followed.

       For 132 kV substations too, it is recommended that bus bar protection be
provided, since failure to clear a bus fault in a short time may lead to wide spread
tripping. The type of bus bar protection scheme recommended for 132 kV system
will depend upon the quantum of power handled and the attendant risks for loss of
power supply and consequential revenue loss.

      Many a times, periodic testing of bus bar protection to check the healthiness
of the relay and associated circuits is difficult since shutdowns of the substations or
bus bars are not easily available. Thus the problems, if any, in the protection or in
the associated circuits, gets discovered only when a fault takes place and either the
relay fails to operate or has operated inadvertently. With modern numerical relays
where self supervision and on line monitoring of the relay and associated circuits are
possible, the task of testing gets simplified considerably and these may be preferred
for this reason. The application of Numerical Relays for bus bar protection therefore
assumes a special status.

8.7   RECOMMENDATIONS FOR DUPLICATING BUS BAR PROTECTIONS
Duplication of bus bar protection is recommended in all substations where failure to
operate may cause disturbances in the grid.

      For the 400 kV and 765 kV substations that fall in this class of substations,
duplication of bus bar protection is strongly recommended. It may be noted that
even those 400 kV substations, which do not fall in this category initially, may
become critical in future as the system grows. In view of constraints in adding a
second bus bar protection at a later date, duplication may be considered desirable
from the initial stage itself.

      In view of continuing thrust on station automation and SCADA application, the
preference towards Numerical Protection schemes for all the elements of a
substation becomes quite beneficial.

## Chapter 9: DC Auxiliary Supply Systems

DC AUXILIARY SUPPLY SYSTEMS
In substations and power plants, DC batteries are used to provide back-up to control
power supply to all the protection, control and automation equipment for fail safe
operation of the plant. They form a reliable, dependable and secured DC Power
Supply Block and form essential part of the protection and control system in the
substation or the power plant and are essential for the reliability of fault clearance.

9.1   CHARACTRISTICS OF DC AUXILIARY SOURCES
The batteries, usually of 220 DC voltage for protection and control of all 220 kV and
above substations and plant (while 48 volt Battery system is used for communication
purposes) are connected to a dedicated charger which is fed by a secure, dedicated
and duplicated auxiliary system AC power supply. The auxiliary supply system is
often provided with duplicated feeders to the chargers and has automatic change
over to diesel generator set, if provided in the substation. Normally the charger feeds
the DC load and also the battery (in float I boost mode). The battery instantly takes
over the load on failure of charger or AC supply. The main parameters of sizing the
battery are:
o     The required autonomy in case of unavailability of the charger varies
      considerably. This can be 1-10 hours in a power plant to several days in
      inaccessible or remote substations. It depends a lot on the intervention delay
      of the maintenance team in charge of the auxiliary supply system.
o     The maximum discharge current required related with 1O-hour discharge rate.
o     Maximum current called by all the equipment functioning together and
      connected simultaneously to the same battery in normal service conditions.
o     It is always desirable to have the load profile indicating the various loads
      related with the hours of service when the AC supply is not available
o     The voltage of the cell at the end of discharge that corresponds to the lowest
      voltage permitted by the various equipment for their proper operation after
      taking in to account the voltage drop in the leads. This voltage is often taken
      equal to 80% of the rated voltage Un.
o     The maximal charge voltage with recommended charge rate and boost charge
      rate up to gassing voltage: This value is linked to the maximum voltage
      acceptable to the various equipment connected, before they start
      malfunctioning.

     Two classes of battery voltage are mainly used: 110-127V and 220-250V.
Generally the 48-52 V supply is used only for telecommunication system.

96                    Manual on Reliable FauN Clearance and Back-Up ProI9ction of
                              EHVand UHV Transmission Networlrs

9.2   STATION BATTERY TECHNOLOGY USED IN SUBSTATIONS
9.2.1 Non-sealed Lead Batteries
There are three types of batteries that are normally used:
•     Accumulators with long life duration plates (Plante plate).
•     Accumulators with pasted plates (Faure type).
•     Accumulators with tubular positive plates (Ironclad plates).

9.2.2 Sealed Lead Batteries with Recombination of Gas
Sealed lead batteries with recombination of gas are sometimes called glass-mat
Valve Regulated Lead Accumulator (VRLA). These accumulators need less
maintenance since the emitted gasses (02 and H2) are recombined to reform the
electrolysed water.

      These batteries have to be operated within certain temperature range in order
to have longer operating life.

9.2.3 Nickel-cadmium Battery
These batteries are lighter than lead batteries for the same capacity and have better
performance with respect to variations in external temperature. Their life duration is
superior to the lead batteries. They require reduced maintenance. However these
are expensive compared to other types of batteries. These batteries are of two
types_
•     Accumulators with "pockets" type plates, an old technology.
•     Accumulators with sintered plates, new technology, whose life duration is
      superior to the old technology.

9.2.4 Types of Batteries and their Selection
Selection of battery is governed by several factors. Key factors, which generally
decide the type of battery set to be used, are as follows.
•     Application and its criticality
•     Type of load, its duration and its nature (Cyclic, continuous, intennittent)
•      Location, manned or unmanned

The practices vary from utility to utility.

                           Chaptsr 9 : DC Auxiliary Supply SysfBms                    97

9.3   DUPLICATION OF AUXILIARY DC SUPPLY SYSTEMS
With high quality DC batteries and good supervision the availability and reliability of
the batteries are satisfactory during their life cycle. The replacement of the battery is
essential when the symptoms defined for the end of their life cycle are observed.

      Each battery is connected to a dedicated charger. The failure of these
chargers is another cause for loss of auxiliary supply. Generally it is supervised and
when a charger fault occurs, an alarm is sent out to control room to inform the
maintenance staff. The current technology trend is towards the use of
microprocessor for the control of battery chargers. In the long term, data on charging
rates and self·diagnostics shall be available via control system of the substation.
This shall then increase the availability of the auxiliary supply.

The following combinations are used for charging the batteries:
•     Single Charger with Battery
•     Two chargers and one Battery (redundancy in charger considering higher
      failure rate)
•     Twin sets of charger and battery.

        The battery capacity is often sufficient to allow the charger replacement or
repairing in time. Thereby the probability of DC auxiliary supply lost by malfunction
of charger is generally very low. The duplicated DC supply is considered essential
for all the substations at 220 kV and above.

       Other causes of loss of auxiliary DC supply such as unwanted opening of DC
circuit breaker or human error during manual intervention exist and its
consequences should be considered while planning the system despite of their low
probability.

      Generally duplication is used on high voltage substations of 220 kV and above
(and some times at 132 kV substations of strategic importance and in 132 kV
substations in generating stations), where redundant protection schemes, each
powered by independent aux power supply are provided. This arrangement rules out
common mode failures.

98                   Manual on Reliable FauN Clearance and Back-Up ProI9ction of
                             EHVand UHV Transmission Networlrs

9.4   DUPLICATION OF DC FUSES ON AUXILIARY SUPPLY
When only one battery is used, the general practice is to provide at least two DC
circuits individually protected by supervised fuse (or suitably rated DC MCB) to
supply the main protection and back-up protection; each supplying its own trip coil
separately. Other arrangements, where more DC feeders are provided, are
described below. Each of these feeders is protected by fuse or a miniature circuit
breaker (MCB).
•     One circuit for Main-l protection.
•     One circuit for back-up protection or Main-2 protection.
•     One circuit for the trip coil 1
•     One circuit for trip coil 2

     At 132 kV substations, single fuse protected circuit is sometimes used by
some utilities.

      The reliability of fuses, when their rating is chosen correctly with respect to the
load and grading required, is quite high. The blowing of fuses is often induced by
human error during an intervention. It is a good practice to supervise each
separately fused circuit with a no volt relay and an alarm sent to the control room.

      Even though reliability of fuses is high, availability of the right fuse element
when replacement is required could be a problem and for this reason use of
miniature circuit breakers of adequate breaking capacity instead of fuses is
recommended.

      The auxiliary contact of such MCBs should be used to send alarm to control
room to indicate their operation. If an auxiliary contact is not available use of no volt
relay shall be made for this purpose.

9.5   DUPLICATION OF TRIP COILS
The battery duplication associated with two main systems of protection completely
independent of each other, implies most of the time, the duplication of trip coils in
order to ensure the complete redundancy of the protection system. This means each
primary system is associated with its own circuit breaker trip coil. Even when the
relay system consists of a high-speed main protection and a low speed back-up
protection, normal practice is to energize one set of trip coils with the main relaying
system and second set with the back-up protection.

       In order to avoid an unwanted breaker failure relay operation, possible
solutions are:
•     The breaker failure protection relay reissues the trip signal through
      instantaneous trip feature to both the trip coils.

                           Chaptsr 9 : DC Auxiliary Supply SysfBms                    99

•     Both trip coils are energized from each relay system i.e., Main-1 and Main-2
      trip both trip coils (cross tripping)

       In case of modern circuit breakers the probability of trip coil failure is low and
its contribution in total failure rate of the circuit breaker is generally negligible.

        Energising the trip coil for too long a time can cause this failure. Human error
and auxiliary contact failures are the main causes for this. The human error is
generally detected and the damaged trip coil is replaced. To take care of failures
due to other causes it is necessary to supervise the trip coil circuit continuously by
providing a trip circuit supervision relay. If there is no supervision of the trip coil
circuit, and such failures are not detected, it might lead to circuit breaker failure.

       In EHVIUHV circuit breakers, though this failure risk is low, it is recommended
to duplicate trip coil on each circuit breaker, with each trip coil being supplied from
different batteries or from a separately fused common battery. Monitoring and
supervision of both trip coils should also be carried out.

9.6   BATTERY GROUND FAULT DETECTORS
Battery ground fault detectors are often used to detect ground faults on either
bus/rail of the battery. The battery ground detector reduces the likelihood of
simultaneous ground faults on both the negative and positive rails, and consequent
loss of the battery supply due to operation of fuse or MCB. Very effective digital
protection and supervision schemes are available for detection of ground faults in
DC system.

9.7   RECOMMENDATIONS FOR DUPLICATION OF DC SUPPLY SYSTEMS
      AND DC DISTRIBUTION SCHEMES
Generally, the use of redundant protection system is done on high voltage
substations of 220 kV and above. In substations where redundant protection
schemes, each powered by independent auxiliary power supply are to be provided,
duplication of DC supply system is recommended. Therefore it is recommended to
provide duplicate DC supply system including battery, battery charger and DC
infeeds and duplicated AC supply to chargers at all 765 kV, 400 kV and 220 kV
substations. This arrangement rules out common mode failures.

      At 132 kV sub-stations including the ones in a power plant duplication of DC
supply system should be done for stations where redundant protection schemes
each powered by separate independent auxiliary power supply is planned.
Otherwise single DC supply system with redundant chargers shall be provided.

      DC distribution shall be done by providing DC feeders that are protected by
fuses or MCBs. Reference may be made to CBIP Manual No 274 "Protection of

100                 Manual on Reliable FauN Clearance and Back-Up ProI9ction of
                            EHVand UHV Transmission Networlrs

Generators, Transformers and 220kV and 400kV Networks" which gives details of
current practices followed for DC distribution arrangements with two battery system_
DC distribution arrangement in case of single battery system can also be on similar
lines_

      Even though reliability of fuses is high, availability of the right fuse element
when replacement is required could be a problem and for this reason use of
miniature circuit breakers of adequate breaking capacity instead of fuses is
recommended_

## Chapter 10: Switching Devices

SWITCHING DEVICES
Circuit breakers are primarily used to interrupt fault currents. In this chapter, the
reliability of circuit breakers, the practice of duplicating the trip coils, and the need for
circuit breaker failure protection are discussed.

      A circuit breaker is required to clear the faults in the system or remove the
abnormalities by isolating the defective system. Circuit breakers interrupt the fault
current when it receives a trip command from the protection system that has
detected the abnormality or power system fault. But the circuit breaker is also
vulnerable to faults and can fail to open and break the fault current. These can then
cause abnormalities in the power system.

        It is therefore necessary to distinguish between two sets of reliability data for
circuit breakers. Firstly, the number of power system faullS that a circuit breaker
clears and secondly, the probability when the circuit breaker fails to clear the fault or
fails to follow the command to open. These two aspects are often put together.

10.1 TYPES OF CIRCUIT BREAKERS
The circuit breaker type is identified by the type of dielectric media used to interrupt
the fault or load current. The types of dielectric used for the EHV circuit breakers are
Oil, Air and SF6 gas. Vacuum circuit breakers are used mainly in medium voltage
applications. From the construction point of view, both for air insulated substations
(AIS) and gas insulated substations (GIS), the various types of circuit breakers in
service are dead tank circuit breakers and live tank circuit breakers. SF6 circuit
breakers are of the most recent technology and have been used extensively since
1975 in the transmission networks.

     The operating mechanisms used are either pneumatic, hydraulic, spring
charged or their combinations.

10.2 REQUIREMENTS ON CIRCUIT BREAKERS
For protection purposes the following requirements are relevant:
•     Operating time

•     Breaking capacity

•     Stuck breaker probability

•     Operating sequence Iduty cycle

102                  Manual on RsliabIB Faun C/sarancs and Back-Up Protection of
                                EHVand UHV Transmission Networlrs

For the design purpose, the following requirements are relevant:
•      Circuit breaker trip coil burden
•      Circuit breaker auxiliary switch contacts to give position indications to the
       protection system

10.3 RELIABILITY OF CIRCUIT BREAKERS
It is important to know the failure rate for switching devices because uncleared
faults, due to failure of circuit breaker to follow the trip command, would cause
extensive damage in the power system. It is also important to know the failure rate
probability of a circuit breaker to fail to open (stuck breaker) and interrupt the fault
current.

      The table given below shows probabilities of circuit breaker not opening on
command or not breaking the current, during manual or automatic opening to
perform switching or to remove a fault. This could be considered as stuck breaker
probability. The probability has decreased from 0.95 to 0.24 stuck breakers per
10,000 commands between 1974-77 and 1988-91. This shows that as technology of
breaking has improved, the probability of stuck breaker has come down.

Table 10.1 CIGRE WG 13.06 survey data on probability of circuit breaker to open or break carried out in
           1988-91

      The CIGRE surveys indicate that the stuck breaker probability is quite low and
the improvement in designs of operating mechanism and devices would in future
further improve the statistics of stuck breakers.

       It is recommended that the utilities maintain the circuit breaker performance
data through appropriate fault reporting procedure and maintenance of records of
circuit breaker operation. This will be useful in planning back-up protection and other
actions pertaining to circuit breaker performance and maintenance.

10.4 DUPLICATION OF TRIP COILS
Most modern EHV systems have duplicated main protections as a standard feature
and the requirement of circuit breakers to have two trip coils. The speed of operation
of circuit breaker will dictate the wattage of trip coils and type of trip coil

                               Chapter 10 : Switching Dsvic:Bs                         103

arrangements. A larger wattage may not be desirable from security point of view.
The trip current to the trip coil will be disconnected by the reliable auxiliary contact of
circuit breakers.

10.5 CIRCUIT BREAKER FAILURE PROTECTION
There is always a risk, however small, that a circuit breaker may fail to obey the trip
command given by protective relays. It would however be possible to assure
successful operation of the circuit breaker to interrupt the load or fault current, by the
duplicate trip coil operation.

       It is to be seen that in the entire substation all the substation elements except
the circuit breaker could be duplicated to ensure successful operation through back-
up operation provided by the redundant system. Unfortunately circuit breaker is the
only item of equipment that does not have any similar element to act as a back-up to
interrupt the fault current in the event of failure of main circuit breaker. As such
breaker back-up is provided by other means through the use of the local breaker
back-up protection to give trip commands to adjacent breakers and breakers at the
remote end. This is usually done through trip logic provided in bus bar protection,
which trips all the breakers connected on the bus in the substation to which the
stuck breaker is connected. Circuit breaker failure protection is used to detect when
circuit breakers fail to open or break. The breaker failure protection belongs to the
back-up protections because it needs some time delay to detect a breaker failure
and is therefore a delayed protection.

       The probability of breaker failure is no doubt quite low. Only about 0.01 % of all
normal switching operations result in a breaker failure. About 0.1 % of all fault
clearance operations may result in a breaker failure. This means that the breaker
failure must possess extreme security to avoid mal-operation when the breaker
operates correctly. At the same time, the breaker failure protection must be very fast
to reduce the back-up fault clearance time. Finally, the breaker failure protection
must be very dependable to clear the fault in case of breaker failure. Several grid
failures in India and abroad leading to blackouts have taken place due to
malfunctioning of Local breaker back-up protection.

10.5.1 The Basic Principle
The block diagram shown in figure 2.3 of chapter 2 gives the flow diagram for
breaker failure protection. Any circuit breaker failure protection works as follows. The
main protection issues a single-pole or three-pole trip command to one or more
circuit breakers. At the same time, the main protection starts and primes the
associated circuit-breaker failure protection system in one or more phases in all
these circuit breakers. At this point, the main protection issues a trip command to the
breaker controlling the faulty circuit. In the event of stuck breaker not following the
command, the LBB relay already primed with fault current still flowing, issues a
command to the trip relay logic in bus bar protection for removing all the breakers on

104               Manual on RsliabIB Faun C/sarancs and Back-Up Protection of
                             EHVand UHV Transmission Networlrs

the bus. There is one fault detector per phase. A fault detector comprises a single-
phase over current relay and may use information from the auxiliary contacts of the
breaker. The fault detector may use several criteria to detect a breaker failure. The
most obvious criterion is that the phase current is higher than a predetermined
value. There is one timer per phase or a common timer for the three phases in each
breaker failure protection. The timer starts when the main protection operates and
starts the breaker failure protection. The setting of the timer should allow the breaker
to open and interrupt the fault current. The breaker failure protection operates when
the timer has operated and the fault detector has identified a breaker failure.

       However, there could be a case of stuck breaker not being removed when the
circuit current is quite low and the LBB could not be primed. The operation of a
Buchholz relay when a faulty transformer is energized from one terminal only is one
such example. In such case the current may be far below the operating value of the
fault detector. Tripping of a generating unit from a reverse power relay is another
case. The current may be as low as 1% of rated current and well below the
operating value of the fault detector. In such cases the best option is that the fault
detector should be provided with information from auxiliary contacts of circuit
breaker, in addition to the current criterion. This will help detect breaker-failures
accompanied with low currents. Information from auxiliary contacts of circuit breaker
without any other criterion will not provide reliable fault detection.

     It is recommended that for operation of Buchholz protection and Reverse
power protection additional criteria from breaker auxiliary contact be provided.

10.5.2 Setting of the Timer
The back-up fault clearance time depends on the setting of the timer in the breaker
failure protection and the operating time of the back-up circuit breakers. The setting
of the timer must be longer than the total interruption time of the main breaker plus
the decision time for the fault detector. Figure 10.1 illustrates the make up of the
total back-up fault clearance time.

      One may decide to plan and operate the power system to avoid transient
instability at shunt faults with a stuck breaker. The back-up fault clearance time then
determines the transfer capability of the transmission network. This means that it is
very important to have a fast breaker failure protection.

      It is desirable that the back-up fault clearance time is shorter than the
operating time of the remote protections. This is more or less a requirement in case
of multi bus bar substations. One would lose the advantages with the expensive bus
bar configuration if Zone-2 of the distance protection in the remote substations
operates faster than the breaker failure protection.

                                 Chapter 10 : Switching Devices                          105

      Main                          Fault
    Protection   Main Breaker      Detector      Timer
                  Interruption                   Relay           Margin
     Operate                        Reset                                   Back-up
                      Time          Time         Error
      Time                                                                  Breaker
                                                                          Interruption
                               Breaker Failure                                Time
                         Timing Relay Operate Time

                    Total Back-up Fault Clearance Time.

                  Fig. 10.1 Total back-up fault clearance time

       It is also possible to use one delay for single-phase faults and a shorter delay
for multi-phase faults. This is done to avoid transient instability at multi-phase faults
in combination with a stuck breaker. The critical fault clearance time is much longer
for single-phase faults than for multi-phase faults. One utility who have adopted this
practice, allow bus tripping in the event of breaker fail, in 120ms for multi-phase
faults and in 240 ms for ground faults.

       For single-phase faults, single-pole tripping and autoreclosing as well as
three-pole tripping and autoreclosing are practiced by utilities in India. It should be
noted that the use of single-pole tripping and reclosing gives higher value of critical
fault clearance time in comparison with the use of three-pole tripping and reclosing
on single-phase faults. It may however be noted that the dead time of high speed
single phase auto-reclosure will be of the order of 1.2 to 1.5 second in order to
ensure successful de-ionisation of secondary arc in the event of multiple lightning
strokes on the line.

10.5.3 Fault Detector
It is necessary to use a fault detector with short and consistent decision time to
obtain a short back-up fault clearance time.

      The main requirements upon the fault detector are as follows. The fault
detector must have -
•       A very high security
•       A short and consistent operating time
•       A high pick up to drop off ratio
•       A lower setting than any protection that starts the breaker failure protection

106                Manual on RsliabIB Faun C/sarancs and Back-Up Protection of
                              EHVand UHV Transmission Networlrs

      The fault detector is, therefore, the most important part of the breaker failure
protection. The fault detector must satisfy stringent requirements under very adverse
conditions. They include: fault current with large DC offset and saturated current
transformers.

       Usually, the fault detector uses an instantaneous over current relay. It is,
however, not necessary that the over current relay distinguishes between fault
current and load current. This is the task of the main protection and it controls the
starting of the breaker failure protection. The over current relay checks whether
current is flowing on the line when the timer has operated.

       In most cases the auxiliary energizing quantity, the DC voltage, is applied to
the over current relay when the main protection has started the breaker failure
protection. The circuit breaker will fail to operate or break if this current relay has not
reset.

       The current detector should have short reset time of the order of 3 to 4 ms.
The reset time can be much longer when a saturated current transformer energizes
the over current relay. The secondary current of the current transformer will not drop
to zero immediately when the circuit breaker interrupts the primary current. The
current transformer generates a DC current when the flux decays from the saturation
flux to the remnant flux. Further the current transformer can go in to saturation and
this may affect the operating time of the breaker failure relay due to pick up and drop
off of current relays in the presence of saturated current wave forms. The current
relay should be designed to take care of these situations.

      Thus the requirements of the current relay can be summarized as under
•     A very high security,
•     A short and consistent operating time
•     Short resetting time
•     High reset ratio
•     Insensitive to the dc component in the secondary current
•     Insensitive to CT saturation
•     A lower setting than any protection that starts the breaker failure protection

      Another requirement on the breaker failure relay is for lines employing single
phase auto reclosing. The current relays should be started on a single-phase basis
from the trip relays for proper operation.

                               Chapter 10 : Switching Dsvic:Bs                          107

10.6 TRIPPING SCHEMES
The breaker failure protection shall trip the adjacent breakers on the bus bars when
it has detected that a breaker has failed to open or break. The adjacent breakers
must then open and interrupt the fault current through the command of bus bar
protection.

     Human errors during preventive maintenance or fault tracing have resulted in
unwanted operation of the breaker failure protection. It is possible to design the
breaker failure protection to have two steps.
•     The first step re·trips its own circuit breaker
•     The second step has a longer delay and trips the adjacent circuit breakers if
      the breaker failure protection does not reset after the re-trip of the breaker.

       This approach may decrease the risk for unwanted operation of the breaker
failure protection during maintenance and fault tracing. Therefore, it is
recommended that utilities consider two-stage tripping, where possibilities of such
unwanted trippings are foreseen.

10.7 ADJACENT CIRCUIT BREAKERS
The breaker failure protection trips the adjacent breakers (other circuit breakers that
are feeding in to the fault) when it has detected that the circuit breaker has failed to
open and break. In principle the adjacent breakers are the circuit breakers
contributing to the fault current. This would require a direct transfer trip from the
breaker failure protection to the circuit breaker at the remote end of a power line with
a stuck breaker. Often, the adjacent breakers are all circuit breakers connected to
the same bus bar as the stuck breaker. The set of adjacent breakers will depend on
the bus bar configuration.

10.8 TRIP COIL AND CLOSING COIL SUPERVISION
Open circuiting of the trip coil or closing coil will result in failure of breaker to isolate
the fault, or failures to auto reclose subsequent to a transient fault. In view of this,
continuous supervision of trip coils and closing coils should be provided. Open
circuit faults in the close or trip coil or discontinuity in the tripping or closing circuit
should give alarm for the operator. It is common practice to provide supervision of
trip coils with provision to get alarm in the EHV/UHV system. Closing coil
supervision is not common except in cases where remote control is adopted.

10.9 SUPERVISION OF OPERATING MECHANISM
To ensure proper operation of circuit breaker, healthiness of operating mechanism is
essential. Leakages in joints, piping etc., can result in loss of operating pressure and
may result in auto trip of the circuit breaker or failure to trip may result in stuck

108               Manual on RsliabIB Faun C/sarancs and Back-Up Protection of
                             EHVand UHV Transmission Networlrs

breaker condition. Two levels of alarms are normally provided to monitor pressure in
case of hydraulic or pneumatic mechanism. In case of spring charged mechanisms
spring charge condition is monitored.

10.10 RECOMMENDATIONS FOR USE OF BREAKER FAIL PROTECTION
Failure of a circuit breaker to open when a trip signal has been given to it can lead to
wide spread tripping. Disconnecting the adjacent breakers using a breaker failure
protection can contain the impact. Failure to provide this protection can lead to
considerable equipment damage and system instability. Therefore breaker fail
protection has an important role to play.

      In the above paragraphs some important application aspects connected with
breaker fail protection and some recommendations have been brought out and
these should be considered. Few of these are brought out below.

•     It is recommended that the utilities maintain the circuit breaker performance
      data, which will be useful in planning back-up protection and other actions
      pertaining to circuit breaker performance and maintenance.
•     One may decide to plan and operate the power system to avoid transient
      instability at shunt faults with a stuck breaker. The back-up fault clearance
      time then determines the power transfer capability of the transmission
      network. This means that it is very important to have a fast breaker failure
      protection.
•     It is desirable that the back-up fault clearance time is shorter than the
      operating time of the remote protections. One would lose the advantages with
      the expensive bus bar configuration, if Zone-2 of the distance protection in the
      remote substations operates faster than the breaker failure protection.
•     It is possible to use one delay for single-phase faults and a shorter delay for
      multi-phase faults in the breaker fail protection. This is done to avoid transient
      instability during multi-phase faults in combination with a stuck breaker. The
      critical fault clearance time is much longer for single-phase faults than for
      multi-phase faults.
•     It is recommended that for operation of Buchholz protection, an additional
      criterion from breaker auxiliary contact may be provided.
•     Another requirement on the breaker failure relay is for lines employing single-
      phase auto reclosing. The current relays should be started on a single-phase
      basis from the trip relays for proper operation.
•     It is possible to design the breaker failure protection to have two steps. This
      approach may decrease the risk for unwanted operation of the breaker failure
      protection during maintenance and fault tracing. Therefore it is recommended

                              Chapter 10 : Switching Dsvic:Bs                        109

      utilities consider two-stage tripping to avoid any unwanted operation of circuit
      breaker fail protection.

      It is a good practice to use breaker failure protection provided in a separate
hardware than the one used for main protection, when a multifunction numerical
protective relay is used for line, transformer, reactor etc. This will help avoid loosing
breaker fail protection function when main protection fails. Thus it can be separate
stand-alone relay or provided in bay controller or as part of bus bar protection. If the
main protections are duplicated and have built in breaker fail function, providing it in
a separate hard ware is not required. In such cases the breaker fail function gets
duplicated.

      As per the current practice breaker failure protection is provided for all
substations at 765 kV, 400 kV, 220 kV and for generating station switchyards. No
change is proposed in this practice. Reference may be made to CBIP Manual No
274 "Protection of Generators, Transformers and 220kV and 400kV Networks",
which gives details of current practices followed.

       For 132 kV substations too, it is recommended that breaker failure protection
be provided since any failure of circuit breaker to open may create wide spread
disturbance.

## Chapter 11: Communication Systems

COMMUNICATION SYSTEMS
Fast selective protections, applied to circuits such as cables or lines, and having
geographically separated terminals, require the interchange of information and
control commands between these terminals. For example, in the case of distance
relays, in the absence of communication links, the operating time for end zone faults
is longer and high-speed single-phase autoreclosing is not possible.

        Protection systems using communication links, also called information links, to
interchange control commands and information provide beller performance
compared to those protections that do not use them. The communication links used
for this purpose are similar to those used for telecommunication.

11.1     PROTECTION SYSTEMS
There are two methods of using communication links to improve the performance of
protections:
•      Non unit protections, which use information from one terminal only
•      Unit protections which use information from all terminals of the protected
       equipment

11.2     BASIC METHODS
There are a number of ways of using an information link to achieve speed and
selective protection. Many factors affect the choice in practice. The methods of using
information links may be broadly classified as follows:
•      Those in which quantitative information is interchanged between the various
       terminals. Examples of this are longitudinal differential protection using pilot
       wires, where the information may be both magnitude and phase of currents,
       and phase-comparison carrier protection, where the information is only phase
       angle.
•      Those in which the information is in the form of a command from one terminal
       to another, which indicates the state of some device, such as a distance relay,
       at the sending terminal.

11.3 COMMAND PROTECTIONS

Protection systems in this class are based on the transmission of simple two-state
information, ''YesINo'' command, from one end of the protected circuit to the other.
The protection equipment sends a command when it detects power system

112               Manual on Reliable Faun C/sar.mce and Back-Up Protsction of
                          EHVand UHV Transmission Networks

abnormality and faults. The protections that send commands can be grouped as
under:
•     Those which send a command to trip
•     Those which send command to block

       The former includes those that perform direct tripping (as for isolation of
unswitched shunt reactor on line) from the received signal, and those that perform
tripping dependent on the conditions of relays at the receiving end aiter receipt of
the command 'to trip".

       In the second case, a block command is in itself sufficient to block the tripping
at the receiving end.

      The choice of protection scheme, e.g., tripping or blocking, and the method by
which the command is transmitted, depends upon a number of factors that include
the type of information links and their susceptibility to interference. The following
sections give typical examples of protections in this class.

11.3.1 Systems Based on a Command "To Trip"
The main forms of protection that fall under this type are:
•     Direct intertripping (sometimes called transfer tripping)
•     Direct tripping command e.g.: for shunt reactor faults. (Such commands are
      usually coded for security reasons)
•     Accelerated distance protection
•     Permissive under reaching transfer tripping (PUTT)
•     Permissive overreaching transfer tripping (POTT)

      In all the cases, the transmission of information from one end to another
indicates that a fault in the forward direction has been detected at the sending end.

      The transmission of information takes place on a faulty line and thus they face
attenuation problems.

11.3.2 Systems Based on a Command "To Block Tripping"
In this class of protection, communication signal (CS) is sent to remote end when
the fault is detected in the reverse direction. Tripping is carried out when this
blocking signal is not received within a certain time (20-40 ms) and the local relay
has detected a fault in the forward direction. To allow for this time, the tripping is
delayed by the time required to receive the signal from remote end.

                                  Chapter 11 : Communication Systems                            113

        Thus the receipt of a signal, blocks the local protection from initiating tripping.
Therefore, in a blocking scheme no tripping signal is transmitted along the faulted
line, instead the signals are transmitted to the remote ends on healthy lines.

      In blocking schemes, the transmission of signal is an essential requirement for
avoiding unwanted tripping on external faults. Any failure of information link does not
generally affect the ability of the protection to trip correctly for internal faults but can
permit unwanted tripping for external faults. Therefore a short transmission time and
good dependability are more important than security.

11.4 COMMON TELEPROTECTION SCHEMES
The different schemes, together with associated zone settings, permissive criteria
and telecommand mode, are summarized in Table 1. Depending upon the
requirements of the systems, there are many variations and combinations of the
basic categories given below:

Table 1 Properties of command protection systems
    Operating mode       Under                 Over-        Permissive        General
                         reaching              reaching     criteria          requirements
                         sending               sending      receiving
    Permissive           Zone-1                             Under impedance   Secure and fast
    Under reach                                             Under voltage
                                                            Over current
                                                            Distance and
                                                            direction
    Permissive                             Zone-2           Distance and      Secure and Fast
    overreach                                               direction
    Direct Trip          Zone-1                             None              Secure &
                                                                              Dependable
    Accelerated          Zone-1                             Zone-2            Secure and Fast
    Under reach
    Blocking overreach                     Reverse          Distance and      Fast and
                                           lookina          direction         Dependable

11.4.1 Permissive Schemes
As mentioned earlier in permissive schemes the communication signal (CS) is sent
to remote end when the fault is detected in forward direction. Tripping is carried out
when the communication signal carrier receive (CR) is received and the local relay
has detected a forward fault.
•       In a permissive under reaching scheme the communication signal is sent from
        a zone that under reaches the remote end.
•       In a permissive overreaching scheme the communication signal is sent from a
        zone that overreaches the remote end.

114               Manual on Reliable Faun C/sar.mce and Back-Up Protsction of
                          EHVand UHV Transmission Networks

11_4_1_1 Permissive under Reach Schemes
In a permissive under reaching scheme, the communication signal is sent from a
zone that under reaches the remote end. Receipt of the signal at the other end
initiates tripping, if the remote end protection at the other end has detected the fault.

       In order to have high security, the receiving end must not be sensitive to false
signals coming from adjacent lines. These false signals are usually generated when
faults occur, or when circuit breaker or isolators operation takes place. Because of
the overreaching of the permissive device, a false signal received can lead to a non-
selective tripping.

       In a double circuit power line, a noise signal can easily be transmitted from the
faulty to the healthy power line due to the mutual coupling between the two circuits.
Precautions must be taken against such non-selective tripping.

11.4.1.2 Permissive Overreach Schemes
In a permissive overreaching scheme, the communication signal is sent from a zone
that overreaches the remote end. Receipt of the signal at the other end initiates
tripping, if the remote end protection has detected the fault.

       The permissive overreaching schemes are advantageous for the protection of
short transmission lines. The reason being the overreaching zones can be set to
detect larger fault resistances compared to under reaching zones and this helps in
detecting high resistance faults in short transmission lines. It can be generally said
that they have the following advantages for short transmission lines.
•     Better performance for high resistance faults
•     Superior to pilot wire as digital decisions are exchanged instead of analogue
      signals.
•     Superior to phase comparison relays which requires faithful communication of
      phase Information

     Teleprotection requirements are similar to those described under section
permissive under reach.

       The operating time of the protection system for all positions of faults on the
protected line circuit includes the overall transmission time, and this should be
relatively short, i.e. of the order of 15-30 ms or less.

11.4.2 Direct Trip
Typical applications for direct transfer tripping are remote tripping for operations of
protections like breaker fail protection and reactor protection intertripping.
Underreach with direct transfer tripping, (line protection) is an exception.

                            Chapter 11 : Communication Systems                       115

       In the case of direct tripping, the tripping command from the teleprotection
equipment goes directly to the circuit breaker tripping coil. Thus a spurious tripping
signal resulting either from interference or human error will cause unwanted, usually
three-phase, tripping of the line and will block the operation of any auto-reclosure
relay. A genuine transfer tripping signal, on the other hand, must on no account be
lost, whether there is interference on the communications channel or not, otherwise
the line fault would not be isolated resuting in serious consequences.

      Extremely high security and high dependability are therefore more important
than transmission time for direct transfer tripping. In order to fulfill these
requirements, coded tripping is used. Coded signals (Frequency shift signals)
provide the necessary additional security against incorrect interpretation of speech,
audio signals coupled into the system and incorrect manipulations on the equipment.
Coded frequency can provide adequate reliability in respect of both dependability
and security with fast overall operating times.

        Normally a redundant channel is used in all cases where direct tripping is
used.

11.4.3 Accelerated Under Reach
This is generally a distance protection using telecommunication, with under reach
protection at each section end, and in which a signal is transmitted when a fault is
detected by the under reach protection. Receipt of the signal at the other end
permits a sequential measurement by an overreach zone to initiate tripping.

       The acceleration scheme in which the basic zone is switched to extend
beyond the basic transmission line protected is not quite as fast in operation as the
other permissive under reach distance schemes. This is because an extra time is
required for the directional measuring unit to make a new measurement and operate
after the range has been extended from Zone-l to Zone-2. However when the
security requirements (to avoid a non-selective operation due to the receipt of a
spurious signal) is dominant, this scheme although slightly slower than the other
permissive schemes, is safer from unwanted operation.

      Reliability requirements on the teleprotection are about the same as for other
permissive schemes, with the difference that the security requirements are slightly
less severe.

11.4.4 Blocking Overreach

Blocking schemes are used when communication signals are not to be transmitted
over faulty line or when boosting of signal is not permitted.

     In this class of protection, communication signal (CS) is sent to remote end
when the fault is detected in the reverse direction. Tripping is carried out when this

116                Manual on Reliable Faun C/sar.mce and Back-Up Protsction of
                           EHVand UHV Transmission Networks

blocking signal is not received within a certain time (20-40 ms) and the local relay
has detected a fault in the forward direction. For a fault on the line, the reverse-
looking directional units at the two ends do not send blocking signals and the
overreaching first zones trip their respective circuit breakers.

       Thus the receipt of a signal blocks the local protection from initiating tripping.
In a blocking scheme no tripping signals are transmitted along the faulted line,
instead the signals are transmitted along the healthy lines to the remote ends for
faults in the reverse direction to prevent tripping of the overreaching protections

       In blocking schemes, the transmission of signal is an essential requirement for
avoiding unwanted tripping on external faults. Any failure of information link does not
generally affect the ability of the protection to trip correctly for internal faults but can
permit unwanted tripping for extemal faults. An incorrect signal for a fault on the
protected line cannot prevent tripping, but only delay it. The loss or appreciable
delay of the blocking signal for an external fault will, however, cause false tripping of
the protected line. Since the overreaching first zone of the relays have to be delayed
sufficiently long to allow time for a blocking signal to be received, a short and
consistent transmission time for the blocking signal is essential. It is important that
the transmission time should not increase due to interference.

     Therefore it follows from these considerations that a short transmission time
and good dependability are more important than security.

      In blocking systems, the transmission of a command is not required in the
case of an internal fault. Thus, internal faults that might delay or interrupt the
telecommand are not a problem, and the additional attenuation normally introduced
by the fault path need not be considered while defining the requirements of PLC link
unlike in the case of permissive systems mentioned under permissive under reach
and accelerated under reach.

      Because of the possibility of a non-selective operation in the case of failure of
the teleprotection, supervision features may be included to change the settings of
the overreaching zones of relays to the normal 70-80% of the protected circuit in
such a cases. Thus it is necessary to monitor the signals continuously both ways or
to provide some forms of automatic self-checking facilities for the channels.

11.4.5 Echo Policies
It could be useful in some teleprotection schemes to return the received signal as a
way to accelerate tripping at the other end. Examples of this application can be
found in weak end in feed condition which can occur on a transmission line, either
when the circuit breaker is open, so there is no current in feed from that line end, or
when the current in feed is low due to weak generation behind the protection. The
following will happen in various schemes of teleprotection described above.

                          Chapter 11 : Communication Systems                    117

•     In permissive overreach schemes both circuit breakers may fail to trip
      instantaneously due to no carrier send signal and no relay operation in weak
      end.
•     In permissive under reach schemes fast fault clearance of the whole line
      section will not be there because no signal will be sent from the weak end.
•     In blocking scheme or permissive under reach scheme the low in feed end will
      fail to trip instantaneously.

      To overcome these problems in lines connecting a strong and a weak station
and in permissive overreaching scheme, the weak end has to be equipped with a
weak in-feed logic and a step of the protection relay will be reverse looking. If a
teleprotection signal is received at the weak end and if the protection does not see
the fault backwards or forwards and there exists an under voltage condition, an
internal fault is assumed and the signal is echoed back allowing tripping. The logic
also sends trip signal to CB on the weak end side. Due to implementation of weak
end in feed logic described above the following will happen.
•     In case of permissive under each scheme the last 10-20% towards weak end
      will be cleared in Zone 2 time. If this is not acceptable overreach scheme
      should be used.
•     In blocking scheme weak end circuit breaker cannot be tripped. In such case
      direct tripping from Zonel and accelerated zone must be used.
•     When operating with one end disconnected or open, it may be useful to
      continuously send permissive / acceleration signal. With this method, the trip
      will be faster as the connected end does not have to wait for the echoed
      signal.

      It is recommended that, on case-to-case basis, utilities consider using echo
signals in the protection systems, as, for example, weak end in feed tripping logic.
Such features are usually available in the modern numerical relays.

11.5 NOISE AND INTERFERENCE CREATED BY THE POWER SYSTEM
Telecommunication systems may fail to perform correctly because of interference
from the power system. Equipment failure and human errors by maintenance staff
are a few other reasons for failure of the system to operate.

      The interference from the power system may exist during normal operation or
may arise at power system faults. The severity of the interference depends on the
signal-to-noise ratio, the spectrum, and the duration and time of interference.

118               Manual on Reliable Faun C/sar.mce and Back-Up Protsction of
                          EHVand UHV Transmission Networks

11_5_1 Perturbations during Normal Operation
11_5_U Corona
The level of noise due to Corona depends on the power system voltage, the climatic
conditions and the type of information link. The presence of Corona does not
generally affect protection, except possibly in some cases of very low power (1 W or
less) Power Line Carrier equipment on 220 kV circuits and above.

       It may be noted that the PLC transmitters used in India normally have peak
envelop power capabilities in the range of 20-80 watts. It may, however, be noted
that for most of the lines the carrier strength of 20 watts meets all the requirement of
adequate signal to noise ratio.

11.5.1.2 Isolator Operation
The operation of an isolator (with total opening time of 6 seconds or so) causes re-
striking arcs at least for 3 seconds for 400 kV systems. They generate high
amplitude bursts of high frequency current. The repetition frequency of the bursts is
in the order of 1kHZ or more. The duration of the pulse-train exceeds 0.5 to 6s. The
pulse train constitutes a high-energy broadband noise source that gives rise to poor
signal-to-noise ratios.

11.5.1.3 Switching by Circuit Breakers
The switching in or out of a circuit, e.g., a line or a transformer, produces high
frequency OSCillation, which is coupled to the equipment in a similar manner as
mentioned under isolator operation. The duration of this type of noise is however
limited to the arcing time of the circuit breaker, and is typically around 20 ms or less.

11.5.2 Perturbations during Power System Disturbances
11.5.2.1 Arcing Faults
At the onset of fault arc and before the arc is fully established, the noise levels are
relatively high and have duration of up to 5ms. When the arc is established, the
noise falls to a lower level. The arc and the noise level remain unaffected until the
circuit breaker operates.

11.5.2.2 Interruption of Fault Current
A breaker generates high-frequency noise at the interruption of fault current. The
duration of such noise is of the order of 1-3 ms and the frequencies lie in the range
up to at least 50 kHZ. The short duration of the noise compared to the response time
of the protection system reduces its significance.

                           Chapter 11 : Communication Systems                       119

11.5.3 Effect of Different Forms of Interference on Teleprotectlon
The importance of the different forms of interference depends on the signal-to-noise
ratios, the frequency spectrum, duration of the interference and the time at which it
takes place. Generally, the type of interference generated under isolator operation is
the most serious because of its high amplitude, wide frequency spectrum, duration
and frequency of occurrence. Because it occurs under normal conditions, it is
important in relation to causing unwanted operation of systems based on a
"command to trip" where permissive features are not used.

      Interference caused during power system faults and their clearance, although
less severe than in case of isolator operation, are important because they occur at
the time during which the teleprotection is in active operation. Furthermore,
protective relays on other circuits may at this time be activated. Interference from
normal circuit-breaker operation and corona are generally the least severe.

11.6 RELIABILITY OF THE INFORMATION LINK
The main parameters of an information link are:
•     Transmission Time
•     Dependability
•     Security
•     Availability

      The optimum compromise between these parameters differs according to the
particular application (blocking, permissive tripping, direct transfer tripping). A
protection-signaling concept is always a compromise; the application defines the
best compromise.

11.6.1 Transmission Time
The transmission time of a teleprotection system is the time elapsed between the
instant of change in state at the command input and the instant of the corresponding
change in state at the command output, excluding propagation time.

      The nominal transmission time To is the time that elapses from the instant a
signal is applied to the input of the teleprotection transmitter until it appears at the
output of the teleprotection receiver. The nominal transmission time To is the
transmission time measured under noise-free transmission conditions. The
measurement is carried out with the transmitter and receiver connected back-to-
back and there is no interference on the channel.

      The maximum actual transmission time Tac is the maximum transmission time
encountered under noisy conditions for a defined dependability and signal-to-noise
(SIN) ratio or bit error rate (BER). The actual transmission time is measured with

120               Manual on Reliable Faun C/sar.mce and Back-Up Protsction of
                          EHVand UHV Transmission Networks

continuous white noise or with random bit errors applied to the transmission path
depending upon the type of teleprotection system.

      Since a longer transmission time enhances signal reliability with respect to
mal-operation, the transmission time should not be chosen shorter than really
required for the application.

11.6.2 Dependability
Dependability relates to the ability to issue and receive a valid command in the
presence of interference and/or noise.

       Noise may disrupt a teleprotection channel by delaying a genuine command
signal or by preventing the receiver from delivering a command.

     Dependability is a measure of the system's ability to receive output trip
commands during adverse signal conditions. It characterizes the receiver's ability to
recognize a genuine tripping signal within a given time in spite of interference on the
communications channel.

11.6.3 Security
Security relates to the ability to prevent interference and noise from generating a
command state at the receiving end when no command signal is transmitted.

     Security is a measure of the communication system's ability not to trip falsely
under adverse signal conditions. Security is the property of the receiver not to
generate spurious tripping signals in the presence of interference on the
communication channel.

11.6.4 Availability
The availability of equipment is also very important. This will depend on the mean
time between failure, MTBF, and the mean time to repair, MTTR, which is the time it
takes to repair a fault.

11.6.5 Recommendations for Measurement of Security and Dependability
Reliability is always a concern for teleprotection systems. Reliability is a compromise
between security and dependability. Security is the ability to properly restrain from
tripping when not called for and dependability is the ability to trip when required.
While security is not improved by increased redundancy, dependability is.

      It is recommended that utilities measure dependability and security of each
teleprotection equipment and keep a record. The data may be based on time
stamped data from teleprotection devices or event loggers. This may be valuable

                           Chapter 11 : Communication Systems                       121

information to monitor the performance of the telecommunication equipment and the
data can be used in taking decisions regarding maintenance, retrofitting and
modernization. It may also be desirable to carry out field tests as a part of
acceptance tests to measure the security and dependability of the carrier signals.

      For detailed definitions of these parameters, reference may be made to IEC
60834-1 Teleprotection equipment of power systems - Performance and Testing
(Partl: Command Systems).

11.7 OUTPUT POWER OF POWER LINE CARRIER SETS
While planning a carrier system it is recommended that, the signal-to-noise ratio
(SNR) is calculated considering the noise level for the various system voltages,
weather conditions, line attenuation at the operating carrier frequencies. If the
calculated SNR is not adequate the output power of the carrier set may have to be
increased. For long power lines this check is particula~y important.

      A typical SNR calculation takes in to account the following parameters into
consideration.
•     Line voltage
•     Line length
•     Line configuration (e.g: conductor diameter, number of bundles and
      transpositions)
•     Frequency band used
•     PLC transmit power
•     Mode of Coupling

       IEC 60663 "Planning of (Single -sideband) Power line carrier system" gives
details of these calculations. The available SNR for PLC links should be better than
the limits specified in this IEC standard, for speech, data and tele-protection signals.

      For a given transmission line, the SNR can be improved by increasing output
power of the carrier set. Better SNR will help the link to perform properly during
adverse and uneven weather conditions.

     For tele-protection, it is recommended to use single tone and the maximum
power for the commands during its transmission. This maintains good SNR for the
commands during interference in the lines and increases the reliability that the
command be received at the other end, thereby improving security and
dependability figures.

122               Manual on Reliable Faun C/sar.mce and Back-Up Protsction of
                          EHVand UHV Transmission Networks

11_8 COUPLING MODES OF TELEPROTECTION CHANNELS
PLC equipment are most commonly used in relaying communication channels
protecting high voltage transmission lines.

       Where phase-to-ground coupling is used for teleprotection channel, it has to
be kept in mind that the phase used for coupling could be seriously affected by a
fault, in which case the efficiency and reliability of the channel will be drastically
reduced.

       Phase-to-phase or inter-circuit or intersystem coupling involves double the
number of coupling elements and consequently more expensive, but it has the
following advantages:
•     The line attenuation will be lower than the phase-to-ground coupling
      arrangement.
•     There is less radiation with phase-to-phase coupling.
•     Greater security, since even if one phase conductor breaks, the other coupling
      continues to work as phase-to-ground system.

       Inter-phase or phase-to-phase coupling provides success probability up to
92%. Though the cost of this is more compared to phase to ground coupling cost, it
is strongly recommended to use this mode of phase-to-phase coupling or intercircuit
coupling when fault clearance time is critical. Therefore the following are
recommended wherever carrier protection is used.
•     Phase- to- phase coupling for 765 kV and 400kV lines.
•     Phase- to- Phase coupling or intercircuit coupling for 220 kV and 132 kV lines.

11.9 ADVANTAGES AND DISADVANTAGES OF THE MOST COMMONLY
      USED LINKS
All communications systems are subject, in varying degrees, to interference and
noise of various forms. These can corrupt the information arriving at the receiver,
either by simulating a signal when no real signal exists, or by preventing or delaying
operation of a real signal. When the signal-to-noise ratio falls to less than some
critical value, the probability of the correct transmission of a message decreases
rapidly and the probability of incorrect and unwanted operation increases. The
critical value is a complex function of the properties of the particular
telecommunication system. There are four possible states of a telecommunication
system when used for protection and these have to be considered in relation to the
transmission and reception of information. They are shown in the Table 2.

                                Chapter 11 : Communication Systems                                     123

Table 2 Response of a teleprotectlon channel
    Condition at communication channel                            Stale 01 protection
    AI sending end              At receiving end
    a)   If a command      is   The command is received and     'Wanted action", i.e., correct Trip
    generated                   obeyed                          or Block is ensured
    b) II a     command    is   The command is not received     "Missing action" i.e. either failure
    generated                   or obeyed                       to trip or failure to block
                                                                (Unwanted operation)
    c) A command     is   not   A    command     is   present   "Unwanted      action"  either
    generated                   received and obeyed             unwanted tripping or unwanted
                                                                blocking

    d) A command     is   not   A command is not present        "No action" correct
    generated

       The design of teleprotection systems, and the ways in which information links
are used, need to take account of practical limitations arising from the fact that
influence of interference cannot be completely avoided. In many cases it is possible
to choose design criteria giving emphasized importance to producing ''wanted
tripping" compared with avoiding "unwanted tripping", or vice versa, in relation to the
effects of interference and/or failure of the telecommunication system. The balance
between these i.e. risk of "unwanted tripping" and reliability of ''wanted tripping"
depends largely on basic considerations such as the requirements of the power
system and the characteristics of the protection system.

        The following are the most commonly used teleprotection equipment used by
utilities in India:
•        Power line carrier (PLC) equipment. This is based on a capacitive connection
         of signals with frequency in the range 32- 500 kHz on the power line.
•        Fiber Optic Links. Optical fibers have the advantage to be insensitive to noise
         and can transmit a huge amount of information.

      Radio I Microwave links are other modes of communication but are not used
for various reasons in India for teleprotection application. Tables 3 and 4
summarizes the advantages and disadvantages of these.

124                    Manual on Reliable Faun C/sar.mce and Back-Up Protsction of
                               EHVand UHV Transmission Networks

Table 3 Properties of power line carrier links
                    Advantages                                            Disadvantages
       •     The overhead power line is normally a           •     Prone to high impulsive noise level
             very reliable transmission medium.                    generated by line faults, lightning and
       •     Long distances, many hundreds of                      isolator breaker operation.
             kilometers can be covered by each link          •     Limited frequency band available. This
             without repeaters.                                    limits the number of PLC links that can
       •     Transmission takes place between the                  work within a given network.
             two stations, which are interconnected          •     Limited bandwidth (4 kHz) restricting the
             for teleprotection purpose.                           minimum transmission time for a
       •     The equipment is situated at the                      teleprotection command system to
             substation, giving easy aceess tor                    approximately 12 ms.
             control and maintenance.                        •     Additional attenuation in case of line
       •     PLC equipment is reliable with a high                 faults.
             MTBF (100 000 to 200 000 hours).                •     Limited     power   due    to   national
       •     It is the most pervasive infrastructure               regulations.
             and therefore has high availability             •     Difficulties in getting the necessary
       •     Existing power lines are used and no                  frequencies    from    the    concerned
             additional cables need to be laid.                    government authorities.
             Therefore tangible cost reduction in
             network development, deployment and
             management

Table 4 Properties of nbsr optic links
           Advantages                                            Disadvantages
       •     Insensitivity to electric and magnetic      •         For long distances, repeaters have to be
             interference fields,      produced by                 used.
             isolator sparks, corona discharge,          •         A break in the fiber will result in the loss
             lightning, radio transmitters etc.                    of a huge amount of information.
       •     Fibers also pose no threat in               •         Installation costs are high.
             dangerous environments such as
             chemical plants where a spark could
                                                         •         The terminations of a fiber optics cable
                                                                   are complex and require special tools.
             trigger an explosion. It doesn't corrode
             and is unaffected by most chemicals.        •         Requires highly skilled labor to
                                                                   terminate. Optical fibers cannot be
       •     Potential isolation between high-                     joined Ispliced together as easily as
             voltage           equipment           and             copper cable and requires additional
             telecommunication equipment.                          training of personnel and expensive
       •     Transmission time is very low                         precision splicing and measurement
       •     No cross-talk problems.                               equipment
       •
       •
             Large bandwidth.
             High transmission speed.
                                                         •         They are more fragile than coaxial cable

       •     Low signal loss and extraordinarily low
             bit error rate.
       •     Their light weight and small size also
             make them ideal for applications
             where running copper cables would be
             impractical
       •     Reduced system costs in terms of
             available band width & Reduced
             maintenance costs
       •     Last but not least is the security
             aspect, it is very, very difficult to tap
             into a fiber cable to read the data
             signals-      secure    communications
             sYstem

                          Chapter 11 : Communication Systems                     125

11.10 REDUNDANCY REQUIREMENTS
Redundancy is defined as 'the existence of more than one means for performing a
given function'. It is obvious that protective relay system dependability can be
increased by added redundancy and if one of the systems does not trip for an in-
zone fault, a redundant system may. Security on the other hand, is generally
decreased by increased redundancy, as there are added devices in the system that
may trip when not called upon to do so. However, redundancy does not influence
dependability and security to the same degree.
       A teleprotection scheme consists of relays, communications interface device
and a communications channel. For relaying, the preferred method of meeting
reliability requirements has been to use physically separate, redundant devices.
      It is generally understood, that teleprotection redundancy will increase the
dependability of the whole system, though it will also increase the possibility of
reduced security, caused by added protection relays and not necessarily due to the
new teleprotection.
      If fault clearance time is critical, back-up teleprotection should be installed
taking into account the following considerations:
•     Dual output contacts and input relays in distance protections.
•     Separate DC battery supply or common DC battery supply separately fused
      for each teleprotection equipment.
•     Separate communication path for redundant audio tone channel.
•     Cross-connection between channels used for Main1 and Main-2 protection.

       It is recommended that redundant channels be provided for very important
lines at 132 and 220 kV level as well as for all lines at 400 kV and 765 kV utilizing
PLCC channels for teleprotection.

      Redundancy in telecommunication equipment may be enhanced as follows:

11.10.1 Redundancy in PLCC Equipment
•     Complete PLC equipment working on the same coupling (balanced combiner
      which splits the signal between the phases) or Ph-Ph coupling.
•     Another PLC equipment coupled to a parallel power transmission line i.e.,
      inter-circuit coupling can also be considered.

11.10.2 Redundancy in Fiber Optic Equipment
11.10.2.1 Redundancy In FIber Cable
•     Two fibers from the same cable
•     Two separate cable routes

126                 Manual on Re/iabIs Faun C/ea/lJllCB and Back·Up Protection of
                             EHVand UHV Transmission Networks

11.10.2.2 Redundancy in Fiber Optic Equipment
•       Two sets of equipment through different fibers of the same cable
•       Two sets of equipment through fibers of different cables
•       Card level redundancy (Power supply card, protection card, CPU board)
•       Use of dual direction fiber optic terminal equipments FOTEs (Type SDH)

11.10.2.3 Example of Fiber Optic in Three-terminal Line Applications
Figure 11.1 shown below gives how redundant communication paths can be
provided in case of three-terminal line application. If a fiber pair already exists
between each line terminal, this is accomplished without any additional
communication interfaces. The pass·through function is using the same
communication heads as the direct communication path. Similar to the double circuit
line application, data from A to B is sent both directly from A to B and on the
redundant channel from A to C to B.

                  Fig. 11.1 Redundant communication paths in case of three-terminal line

11.11     RECOMMENDATIONS FOR SELECTION OF COMMUNICATION
          CHANNELS
Security of a teleprotection system can go down if the communication channel is not
of high security. In most cases power line carrier (PLC) is widely used. As brought
out earlier Fiber optic is superior to PLC and is quite versatile. Therefore it is
recommended that wherever possible Main-I protection should be equipped with the
best of teleprotection equipment, for example Fiber Optic communication using
OPGW.

                          Chapter 11 : Communication Systems                      127

      Especially for lines and cables it is also very important that Main-I protection
and Main-2 protections cover part of the protected equipment zone, independent of
the communication channel, to provide fast opening of the local circuit-breaker. Thus
use of a non unit protection like distance relay as one of the main protection,is a
must.This action is very useful to accomplish system stability, though, generally,
time of clearance will be greater under some conditions (one end open).

      In this chapter some important aspects connected with the communication
system and some recommendations have been brought out and these should be
considered. Few of these are brought out below:
•     It is recommended that redundant channels should be provided for very
      important lines at 132 and 220 kV level and for all lines at 400 kV and 765 kV
      utilizing PLCC channels for teleprotection.
•     Utilities should measure dependability and security of each teleprotection
      equipment and keep a record. This may be valuable information to monitor the
      performance of the telecommunication equipment and the data can be used in
      taking decisions regarding maintenance, retrofitting and modernization.
•     While planning a carrier system it is recommended that, the signal-to-noise
      ratio (SNR) is calculated considering the noise level for the various system
      voltages, weather conditions, line attenuation at the operating carrier
      frequencies. If the calculated SNR is not adequate the output power of the
      carrier set may have to be increased. For long power lines this check is
      particula~y important.

•     In case of PLCC, Inter-phase or Phase-to-Phase coupling provides high
      success probability. Therefore, Phase-to-phase coupling for 765 kV and
      400kV lines, Phase- to- Phase coupling or inter circuit coupling for 220 kV and
      132 kV lines is recommended to be used
•     In case of short transmission lines, when distance protections are applied, the
      permissive overreaching schemes are advantageous for detection of high
      resistance faults and are therefore to be used.
•     On case-to-case basis, utilities should consider using echo signals in the
      protection systems, as, for example, week end in feed tripping logic.

## Chapter 12: References

REFERENCES
(1)   CIGRE 34 WG: 01 report "Reliable fault clearance and back up protection"
(2)   "Back-up protections on the ESKOM transmission network: philosophy review
      and considerations". CIGRE SC 34 colloquium South Africa 1997
(3)   Papers on preferential subject#2:Back-up Protection.        CIGRE SC 34
      colloquium South Africa 1997
(4)   CIGRE WG 34.04 in 1991 "Application guide on protection of complex
      transmission network configurations"
(5)   CIGRE: SC-34 WG report "Transformer Over fluxing Protection" ELECTRA
      (N031). 1973
(6)   IEC 60834-1 "Teleprotection equipment of power systems Performance and
      Testing ( Part1 :Command Systems)"
(7)   IEC 60663 "Planning of ( Single -Side band) Power line carrier systems"
(8)   CBIP manual No 274 "Protection of Generators. Generator Transformers and
      220 KV and 400 KV Networks"
(9)   Central Electricity Authority New Delhi report "Manual on transmission
      planning criteria"
