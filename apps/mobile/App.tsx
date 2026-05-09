import React, { useEffect, useState } from 'react';
import { View, Text, ScrollView, TouchableOpacity, ActivityIndicator, Platform, Dimensions } from 'react-native';
import { StatusBar } from 'expo-status-bar';

import { Pill, Calendar, Bell, Heart, User, ChevronRight, CheckCircle2 } from 'lucide-react-native';

const { width } = Dimensions.get('window');
const API_URL = 'http://172.16.3.147:8080'; // Your host machine IP

export default function App() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch(`${API_URL}/api/patients/me`, {
          method: 'GET',
          headers: { 'Accept': 'application/json' }
        });
        if (!response.ok) throw new Error('Backend error');
        const json = await response.json();
        setData(json);
      } catch (err) {
        console.warn("Backend connection failed:", err.message);
        setError("Local Server Offline");
        setData({ name: "Lakshmi", streak: 12 });
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  if (loading) {
    return (
      <View style={{ flex: 1, backgroundColor: '#0f172a', alignItems: 'center', justifyContent: 'center' }}>
        <ActivityIndicator size="large" color="#6366f1" />
        <Text style={{ marginTop: 20, color: '#94a3b8', fontSize: 16 }}>Syncing with CARA...</Text>
      </View>
    );
  }

  return (
    <View style={{ flex: 1, backgroundColor: '#f8fafc' }}>
      <StatusBar style="dark" />
      
      {/* Premium Header */}
      <View style={{ paddingTop: 60, paddingHorizontal: 24, paddingBottom: 20, backgroundColor: '#fff' }}>
        <View style={{ flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center' }}>
          <View>
            <Text style={{ fontSize: 14, color: '#64748b', fontWeight: '600' }}>GOOD MORNING</Text>
            <Text style={{ fontSize: 28, fontWeight: '800', color: '#1e293b' }}>{data?.name || "Patient"}</Text>
          </View>
          <TouchableOpacity style={{ backgroundColor: '#f1f5f9', padding: 12, borderRadius: 16 }}>
            <User size={24} color="#6366f1" />
          </TouchableOpacity>
        </View>
      </View>

      <ScrollView style={{ flex: 1 }} contentContainerStyle={{ paddingHorizontal: 24, paddingBottom: 40 }}>
        
        {/* Connection Status Badge */}
        {error ? (
          <View style={{ backgroundColor: '#fff7ed', padding: 10, borderRadius: 12, marginBottom: 20, flexDirection: 'row', alignItems: 'center', borderWeight: 1, borderColor: '#ffedd5' }}>
            <View style={{ width: 8, height: 8, borderRadius: 4, backgroundColor: '#f97316', marginRight: 8 }} />
            <Text style={{ color: '#c2410c', fontSize: 12, fontWeight: '700' }}>DEV MODE: {error}</Text>
          </View>
        ) : (
          <View style={{ backgroundColor: '#f0fdf4', padding: 10, borderRadius: 12, marginBottom: 20, flexDirection: 'row', alignItems: 'center' }}>
            <View style={{ width: 8, height: 8, borderRadius: 4, backgroundColor: '#22c55e', marginRight: 8 }} />
            <Text style={{ color: '#15803d', fontSize: 12, fontWeight: '700' }}>CONNECTED TO CARA SECURE CLOUD</Text>
          </View>
        )}

        {/* Streak Hero Card - Fixed with Solid Background for Stability */}
        <View
          style={{ backgroundColor: '#6366f1', borderRadius: 32, padding: 24, marginBottom: 24, elevation: 8, shadowColor: '#6366f1', shadowOffset: { width: 0, height: 10 }, shadowOpacity: 0.3, shadowRadius: 20 }}
        >
          <View style={{ flexDirection: 'row', justifyContent: 'space-between', alignItems: 'flex-start' }}>
            <View>
              <Text style={{ color: 'rgba(255,255,255,0.8)', fontWeight: '600', fontSize: 14 }}>ADHERENCE STREAK</Text>
              <Text style={{ color: '#fff', fontSize: 42, fontWeight: '900', marginTop: 4 }}>{data?.streak || 12} <Text style={{ fontSize: 20 }}>DAYS</Text></Text>
            </View>
            <View style={{ backgroundColor: 'rgba(255,255,255,0.2)', padding: 12, borderRadius: 20 }}>
              <Heart size={28} color="#fff" />
            </View>
          </View>
          
          <View style={{ height: 8, backgroundColor: 'rgba(255,255,255,0.2)', borderRadius: 4, marginTop: 24, overflow: 'hidden' }}>
            <View style={{ width: '85%', height: '100%', backgroundColor: '#fff', borderRadius: 4 }} />
          </View>
          <Text style={{ color: 'rgba(255,255,255,0.9)', marginTop: 12, fontSize: 14, fontWeight: '500' }}>Top 5% of heart-health champions this month!</Text>
        </View>

        {/* Medication Schedule Section */}
        <View style={{ flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16 }}>
          <Text style={{ fontSize: 20, fontWeight: '800', color: '#1e293b' }}>Today's Routine</Text>
          <TouchableOpacity>
            <Text style={{ color: '#6366f1', fontWeight: '700' }}>View Schedule</Text>
          </TouchableOpacity>
        </View>

        {/* Med Card 1 */}
        <View style={{ backgroundColor: '#fff', borderRadius: 24, padding: 20, marginBottom: 16, flexDirection: 'row', alignItems: 'center', borderWeight: 1, borderColor: '#f1f5f9', elevation: 2, shadowColor: '#000', shadowOffset: { width: 0, height: 2 }, shadowOpacity: 0.05, shadowRadius: 8 }}>
          <View style={{ width: 56, height: 56, borderRadius: 18, backgroundColor: '#eef2ff', alignItems: 'center', justifyContent: 'center' }}>
            <Pill size={28} color="#6366f1" />
          </View>
          <View style={{ flex: 1, marginLeft: 16 }}>
            <Text style={{ fontSize: 18, fontWeight: '700', color: '#1e293b' }}>Metformin</Text>
            <Text style={{ fontSize: 14, color: '#64748b', marginTop: 2 }}>500mg • After Breakfast</Text>
          </View>
          <View style={{ alignItems: 'flex-end' }}>
            <Text style={{ fontSize: 14, fontWeight: '800', color: '#6366f1' }}>08:00 AM</Text>
            <View style={{ marginTop: 6, backgroundColor: '#f0fdf4', paddingHorizontal: 8, paddingVertical: 4, borderRadius: 8 }}>
              <Text style={{ fontSize: 10, color: '#15803d', fontWeight: '800' }}>TAKEN</Text>
            </View>
          </View>
        </View>

        {/* Med Card 2 (Actionable) */}
        <TouchableOpacity style={{ backgroundColor: '#fff', borderRadius: 24, padding: 20, marginBottom: 24, flexDirection: 'row', alignItems: 'center', borderWeight: 2, borderColor: '#6366f1', elevation: 4, shadowColor: '#6366f1', shadowOffset: { width: 0, height: 4 }, shadowOpacity: 0.1, shadowRadius: 12 }}>
          <View style={{ width: 56, height: 56, borderRadius: 18, backgroundColor: '#6366f1', alignItems: 'center', justifyContent: 'center' }}>
            <Bell size={28} color="#fff" />
          </View>
          <View style={{ flex: 1, marginLeft: 16 }}>
            <Text style={{ fontSize: 18, fontWeight: '700', color: '#1e293b' }}>Atorvastatin</Text>
            <Text style={{ fontSize: 14, color: '#64748b', marginTop: 2 }}>20mg • Before Lunch</Text>
          </View>
          <ChevronRight size={24} color="#cbd5e1" />
        </TouchableOpacity>

        {/* Dosi Assistant Card */}
        <View style={{ backgroundColor: '#1e293b', borderRadius: 32, padding: 24, overflow: 'hidden' }}>
          <View style={{ flexDirection: 'row', alignItems: 'center', marginBottom: 12 }}>
            <View style={{ width: 40, height: 40, borderRadius: 20, backgroundColor: '#fff', alignItems: 'center', justifyContent: 'center', marginRight: 12 }}>
              <Text style={{ fontSize: 20 }}>🐼</Text>
            </View>
            <Text style={{ color: '#fff', fontSize: 18, fontWeight: '800' }}>Dosi is here</Text>
          </View>
          <Text style={{ color: '#94a3b8', fontSize: 16, lineHeight: 24 }}>
            "Lakshmi, your heart rate was slightly higher this morning. Remember to sit still for 5 minutes before your lunch meds."
          </Text>
          <TouchableOpacity style={{ marginTop: 20, backgroundColor: '#334155', alignSelf: 'flex-start', paddingHorizontal: 16, paddingVertical: 10, borderRadius: 12 }}>
            <Text style={{ color: '#fff', fontWeight: '700' }}>Thanks, Dosi!</Text>
          </TouchableOpacity>
        </View>

      </ScrollView>
    </View>
  );
}
