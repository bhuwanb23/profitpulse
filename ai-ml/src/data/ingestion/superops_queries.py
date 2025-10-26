"""
SuperOps GraphQL Queries
Pre-defined GraphQL queries for SuperOps API integration
"""

from gql import gql

# Ticket List Query
GET_TICKETS_QUERY = gql("""
    query getTicketList($input: ListInfoInput!) {
      getTicketList(input: $input) {
        tickets {
          ticketId
          displayId
          subject
          status
          priority
          createdTime
          updatedTime
          firstResponseTime
          resolutionTime
          firstResponseViolated
          resolutionViolated
          technician { 
            userId 
            name 
          }
          requester { 
            userId 
            name 
          }
          site { 
            id 
            name 
          }
          worklogTimespent
          customFields {
            fieldName
            fieldValue
          }
          tags
        }
        listInfo {
          page
          pageSize
          hasMore
          totalCount
        }
      }
    }
""")

# SLA List Query
GET_SLA_LIST_QUERY = gql("""
    query getSLAList {
      getSLAList {
        id
        name
        description
        responseTime
        resolutionTime
        isActive
      }
    }
""")

# Technician List Query
GET_TECHNICIANS_QUERY = gql("""
    query getTechnicianList($input: ListInfoInput!) {
      getTechnicianList(input: $input) {
        userList {
          userId
          name
          email
          phone
          department { 
            departmentId 
            name 
          }
          groups { 
            groupId 
            name 
          }
          skills
          certifications
          hourlyRate
          availability
          performanceScore
          ticketsResolved
          avgResolutionTime
          customerSatisfaction
          createdDate
          lastActive
        }
        listInfo {
          page
          pageSize
          totalCount
        }
      }
    }
""")

# Site List Query
GET_SITES_QUERY = gql("""
    query getSiteList($input: ListInfoInput!) {
      getSiteList(input: $input) {
        sites {
          id
          name
          contactNumber
          email
          address {
            line1
            line2
            city
            stateCode
            countryCode
            zipCode
          }
          industry
          companySize
          contractType
          contractValue
          contractStartDate
          contractEndDate
          billingFrequency
          paymentTerms
          primaryContact
          secondaryContact
          serviceLevel
          customFields {
            fieldName
            fieldValue
          }
          tags
          createdDate
          lastActivity
        }
        listInfo {
          page
          pageSize
          totalCount
        }
      }
    }
""")

# Asset List Query
GET_ASSETS_QUERY = gql("""
    query getAssetList($input: ListInfoInput!) {
      getAssetList(input: $input) {
        assets {
          assetId
          name
          site { 
            id 
            name 
          }
          status
          lastCommunicatedTime
          platformCategory
          assetType
          manufacturer
          model
          serialNumber
          warrantyExpiry
          purchaseDate
          purchasePrice
          customFields {
            fieldName
            fieldValue
          }
          tags
        }
        listInfo {
          page
          pageSize
          totalCount
        }
      }
    }
""")

# Service Delivery Metrics Query
GET_SERVICE_METRICS_QUERY = gql("""
    query getServiceMetrics($input: ServiceMetricsInput!) {
      getServiceMetrics(input: $input) {
        date
        totalTickets
        resolvedTickets
        openTickets
        avgResolutionTime
        slaComplianceRate
        customerSatisfaction
        technicianUtilization
        revenueGenerated
        costPerTicket
      }
    }
""")

# Real-time Data Query
GET_REALTIME_DATA_QUERY = gql("""
    query getRealtimeData {
      getRealtimeData {
        timestamp
        activeTickets
        pendingTickets
        onlineTechnicians
        slaBreachesToday
        avgResponseTime
        systemHealth
        alerts {
          type
          message
          severity
          timestamp
        }
      }
    }
""")

# Technician Productivity Query
GET_TECHNICIAN_PRODUCTIVITY_QUERY = gql("""
    query getTechnicianProductivity($input: TechnicianProductivityInput!) {
      getTechnicianProductivity(input: $input) {
        technicianId
        period
        ticketsResolved
        avgResolutionTime
        customerSatisfaction
        utilizationRate
        overtimeHours
        skillsUtilized
        performanceScore
        improvementAreas
      }
    }
""")
